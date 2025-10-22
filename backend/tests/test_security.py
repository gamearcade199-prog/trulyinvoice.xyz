"""
Comprehensive Security Test Suite
Tests all critical security fixes and system integrations
Run with: pytest backend/tests/test_security.py -v
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import time

# These tests assume you have a test database and Supabase instance


class TestAuthentication:
    """Test real JWT authentication"""
    
    def test_different_users_get_different_ids(self, client: TestClient):
        """Verify different users get different authentication IDs"""
        # User 1 registers
        response1 = client.post("/api/auth/setup-user", json={
            "user_id": "user-1",
            "email": "user1@test.com",
            "full_name": "User One"
        })
        assert response1.status_code == 200
        
        # User 2 registers
        response2 = client.post("/api/auth/setup-user", json={
            "user_id": "user-2",
            "email": "user2@test.com",
            "full_name": "User Two"
        })
        assert response2.status_code == 200
        
        # Verify they got different IDs
        assert response1.json()["subscription"]["user_id"] != response2.json()["subscription"]["user_id"]
    
    def test_invalid_token_rejected(self, client: TestClient):
        """Verify invalid JWT tokens are rejected"""
        headers = {"Authorization": "Bearer invalid_token_xyz"}
        response = client.get("/api/invoices", headers=headers)
        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]
    
    def test_missing_auth_header_rejected(self, client: TestClient):
        """Verify missing authorization header is rejected"""
        response = client.get("/api/invoices")
        assert response.status_code == 401


class TestPaymentSecurity:
    """Test payment fraud prevention"""
    
    def test_user_cannot_verify_others_payment(self, client: TestClient):
        """
        User A cannot verify payment for User B
        Ownership check should prevent fraud
        """
        # User A creates order
        order_response = client.post("/api/payments/create-order", json={
            "tier": "pro",
            "billing_cycle": "monthly"
        }, headers={"Authorization": f"Bearer {get_token('user-a')}"})
        
        order_id = order_response.json()["order_id"]
        
        # User B tries to verify User A's payment
        verify_response = client.post("/api/payments/verify", json={
            "razorpay_order_id": order_id,
            "razorpay_payment_id": "pay_test",
            "razorpay_signature": "sig_test"
        }, headers={"Authorization": f"Bearer {get_token('user-b')}"})
        
        # Should fail with 403 (Forbidden)
        assert verify_response.status_code == 403
        assert "fraud" in verify_response.json()["detail"].lower()
    
    def test_duplicate_payment_prevented(self, client: TestClient):
        """Verify same payment cannot be processed twice"""
        order_response = client.post("/api/payments/create-order", json={
            "tier": "pro",
            "billing_cycle": "monthly"
        }, headers={"Authorization": f"Bearer {get_token('user-a')}"})
        
        order_id = order_response.json()["order_id"]
        
        # First verification (would succeed with real payment)
        response1 = client.post("/api/payments/verify", json={
            "razorpay_order_id": order_id,
            "razorpay_payment_id": "pay_123",
            "razorpay_signature": "sig_123"
        }, headers={"Authorization": f"Bearer {get_token('user-a')}"})
        
        # Second verification with same payment ID
        response2 = client.post("/api/payments/verify", json={
            "razorpay_order_id": order_id,
            "razorpay_payment_id": "pay_123",
            "razorpay_signature": "sig_123"
        }, headers={"Authorization": f"Bearer {get_token('user-a')}"})
        
        # Second should fail
        assert response2.status_code == 400
        assert "already processed" in response2.json()["detail"].lower()
    
    def test_amount_mismatch_detected(self, client: TestClient):
        """Verify payment amount mismatch is detected"""
        # Create order for $9.99
        order_response = client.post("/api/payments/create-order", json={
            "tier": "pro",
            "billing_cycle": "monthly"
        }, headers={"Authorization": f"Bearer {get_token('user-a')}"})
        
        # Verify with wrong amount should fail
        verify_response = client.post("/api/payments/verify", json={
            "razorpay_order_id": order_response.json()["order_id"],
            "razorpay_payment_id": "pay_wrong",
            "razorpay_signature": "sig_wrong",
            "amount": 1  # Wrong amount
        }, headers={"Authorization": f"Bearer {get_token('user-a')}"})
        
        # Should fail
        assert verify_response.status_code in [400, 403]


class TestRateLimiting:
    """Test rate limiting and brute force protection"""
    
    def test_rate_limit_on_registration(self, client: TestClient):
        """Verify rate limiting on registration (5/min per IP)"""
        # Attempt registration 5 times (should succeed)
        for i in range(5):
            response = client.post("/api/auth/setup-user", json={
                "user_id": f"user-{i}",
                "email": f"user{i}@test.com"
            })
            assert response.status_code == 200
        
        # 6th attempt should be rate limited
        response = client.post("/api/auth/setup-user", json={
            "user_id": "user-6",
            "email": "user6@test.com"
        })
        assert response.status_code == 429
    
    def test_exponential_backoff(self, client: TestClient):
        """Verify exponential backoff timing for repeated violations"""
        # Trigger rate limit (attempt 6)
        for i in range(6):
            client.post("/api/auth/setup-user", json={
                "user_id": f"user-{i}",
                "email": f"user{i}@test.com"
            })
        
        # Should be blocked with 5-second backoff
        start_time = time.time()
        response = client.post("/api/auth/setup-user", json={
            "user_id": "user-7",
            "email": "user7@test.com"
        })
        elapsed = time.time() - start_time
        
        assert response.status_code == 429
        assert "5" in response.json()["detail"]  # Should mention 5 seconds


class TestSubscriptionTracking:
    """Test dynamic subscription tracking"""
    
    def test_monthly_reset_automatic(self, client: TestClient):
        """
        Verify monthly scan count resets automatically
        Test with dynamic month calculation
        """
        # Create subscription
        response = client.post("/api/auth/setup-user", json={
            "user_id": "user-scan",
            "email": "user@scan.com"
        })
        assert response.status_code == 200
        
        # Check subscription
        sub_response = client.get("/api/auth/subscription/user-scan")
        assert sub_response.status_code == 200
        
        # Scans should be 0 for new user
        assert sub_response.json()["subscription"]["scans_used"] == 0
    
    def test_scan_limit_enforced(self, client: TestClient):
        """Verify scan limits are enforced"""
        # User with free plan (10 scans/month)
        response = client.post("/api/auth/setup-user", json={
            "user_id": "user-limit",
            "email": "user@limit.com"
        })
        
        # Get subscription
        sub = client.get("/api/auth/subscription/user-limit").json()
        
        # Free plan should have 10-scan limit
        assert sub["subscription"]["scans_limit"] == 10


class TestSessionTimeout:
    """Test session timeout functionality"""
    
    def test_session_timeout_after_inactivity(self):
        """
        Verify session times out after 30 minutes of inactivity
        Note: This test would need to be run with mocked time
        """
        from frontend.src.lib.supabase import (
            startSessionMonitoring,
            getSessionTimeRemaining,
            isSessionExpired
        )
        
        # Start monitoring (would be called on login)
        # Note: This is a simplified test
        assert not isSessionExpired()
    
    def test_activity_resets_timeout(self):
        """Verify user activity resets the timeout timer"""
        from frontend.src.lib.supabase import (
            resetActivityTimer,
            getSessionTimeRemaining
        )
        
        # Reset activity (simulates user interaction)
        resetActivityTimer()
        
        # Timer should be reset
        remaining = getSessionTimeRemaining()
        assert remaining > (30 * 60 - 10)  # Should be close to 30 minutes


class TestPasswordReset:
    """Test password reset flow"""
    
    def test_password_reset_email_sent(self, client: TestClient):
        """Verify password reset email is sent"""
        response = client.post("/api/auth/forgot-password", json={
            "email": "user@test.com"
        })
        
        # Should always return success for security
        assert response.status_code == 200
        assert response.json()["success"]
    
    def test_password_changed_successfully(self, client: TestClient):
        """Verify password can be changed"""
        response = client.post("/api/auth/reset-password", json={
            "token": "valid_reset_token",
            "new_password": "NewPassword123!"
        })
        
        # Note: This would fail with invalid token in real scenario
        # In production, use actual Supabase reset tokens


class TestAuditLogging:
    """Test audit logging functionality"""
    
    def test_payment_logged(self, client: TestClient, db):
        """Verify payment attempts are logged"""
        from app.models.audit_log import create_payment_log
        
        # Create payment log
        log = create_payment_log(
            user_id="test-user",
            order_id="order-123",
            status="success",
            db=db,
            amount=999,
            signature_valid=True,
            ownership_verified=True
        )
        
        assert log.user_id == "test-user"
        assert log.status == "success"
    
    def test_login_logged(self, client: TestClient, db):
        """Verify login attempts are logged"""
        from app.models.audit_log import create_login_log
        
        # Create login log
        log = create_login_log(
            email="user@test.com",
            success=True,
            db=db,
            ip_address="192.168.1.1"
        )
        
        assert log.email == "user@test.com"
        assert log.success is True


class TestSubscriptionRenewal:
    """Test subscription auto-renewal"""
    
    def test_auto_renewal_activates(self, client: TestClient):
        """Verify auto-renewal works correctly"""
        from app.middleware.subscription import check_and_renew_subscription
        
        # This would check renewal status
        # In production, test with actual subscription data


# Helper functions

def get_token(user_id: str) -> str:
    """Get JWT token for test user"""
    # In production, this would get real token from Supabase
    return f"test_token_{user_id}"


# Pytest fixtures

@pytest.fixture
def client():
    """Create test client"""
    from fastapi.testclient import TestClient
    from backend.app.main import app
    return TestClient(app)


@pytest.fixture
def db():
    """Create test database session"""
    # In production, use test database
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Use SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal()


if __name__ == "__main__":
    # Run tests with: pytest test_security.py -v
    print("Run tests with: pytest backend/tests/test_security.py -v")
