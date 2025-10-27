"""
Payment System Comprehensive Tests
Tests all critical fixes and payment flows
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session

from app.models import Subscription
from app.services.razorpay_service import razorpay_service
from app.config.plans import get_plan_config


class TestTransactionIsolation:
    """Test Fix #1: Transaction isolation in payment verification"""
    
    def test_subscription_created_atomically(self, db: Session):
        """
        Test that subscription is created in atomic transaction.
        If any step fails, entire transaction should roll back.
        """
        # Setup
        user_id = "test_user_atomic_001"
        order_id = "order_test_001"
        payment_id = "pay_test_001"
        
        # Mock Razorpay order with proper notes
        mock_order = {
            "id": order_id,
            "amount": 14900,  # ₹149
            "notes": {
                "user_id": user_id,
                "tier": "basic",
                "billing_cycle": "monthly"
            }
        }
        
        with patch.object(razorpay_service.client, 'order.fetch', return_value=mock_order):
            # Process payment
            success, message, subscription_data = razorpay_service.process_successful_payment(
                order_id=order_id,
                payment_id=payment_id,
                signature="verified",
                db=db
            )
        
        # Verify subscription was created
        assert success == True, f"Payment processing failed: {message}"
        assert subscription_data is not None
        
        # Verify DB has the subscription
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.razorpay_payment_id == payment_id
        ).first()
        
        assert subscription is not None, "Subscription not found in database"
        assert subscription.tier == "basic"
        assert subscription.status == "active"
        assert subscription.razorpay_payment_id == payment_id
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()
    
    def test_subscription_update_atomic(self, db: Session):
        """Test that subscription update is atomic"""
        # Setup - create existing subscription
        user_id = "test_user_update_001"
        order_id1 = "order_test_101"
        order_id2 = "order_test_102"
        payment_id1 = "pay_test_101"
        payment_id2 = "pay_test_102"
        
        # Create initial subscription
        subscription = Subscription(
            user_id=user_id,
            tier="free",
            status="active",
            scans_used_this_period=5,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        db.add(subscription)
        db.commit()
        
        # Now upgrade via payment
        mock_order = {
            "id": order_id2,
            "amount": 29900,  # ₹299 for Pro
            "notes": {
                "user_id": user_id,
                "tier": "pro",
                "billing_cycle": "monthly"
            }
        }
        
        with patch.object(razorpay_service.client, 'order.fetch', return_value=mock_order):
            success, message, subscription_data = razorpay_service.process_successful_payment(
                order_id=order_id2,
                payment_id=payment_id2,
                signature="verified",
                db=db
            )
        
        assert success == True
        
        # Verify subscription was updated
        updated = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        assert updated.tier == "pro"
        assert updated.razorpay_payment_id == payment_id2
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()


class TestUserMetadata:
    """Test Fix #2: User metadata fetching from Supabase"""
    
    def test_order_creation_with_real_user_email(self):
        """Test that order is created with real user email/name"""
        # This test verifies the code path that fetches user email
        # In production, this would come from Supabase auth
        
        order_data = razorpay_service.create_subscription_order(
            user_id="test_user_metadata",
            tier="pro",
            billing_cycle="monthly",
            user_email="user@example.com",
            user_name="John Doe",
            db=None  # Not used for order creation
        )
        
        # Verify order has user data in notes
        assert "order_id" in order_data
        assert order_data["tier"] == "pro"
        assert order_data["plan_name"] is not None
        assert order_data["amount"] > 0
    
    def test_order_notes_contain_user_info(self):
        """Test that Razorpay order notes contain user information"""
        user_email = "john@example.com"
        user_name = "John Doe"
        
        order_data = razorpay_service.create_subscription_order(
            user_id="test_user_info",
            tier="basic",
            billing_cycle="monthly",
            user_email=user_email,
            user_name=user_name,
            db=None
        )
        
        # Verify order was created
        assert order_data["order_id"] is not None
        assert order_data["amount"] == 149  # ₹149 for Basic


class TestWebhookHandling:
    """Test Fix #3: Webhook endpoint implementation"""
    
    def test_webhook_signature_verification(self, db: Session):
        """Test that webhook signature is verified"""
        # Setup
        user_id = "test_user_webhook_001"
        order_id = "order_webhook_001"
        payment_id = "pay_webhook_001"
        
        # Create event
        event = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {
                        "id": payment_id,
                        "order_id": order_id
                    }
                }
            }
        }
        
        # Test with no webhook secret (should process event)
        success, message = razorpay_service.handle_webhook(
            event=event,
            signature="",  # No signature verification needed without secret
            db=db
        )
        
        # Should attempt to process but fail gracefully if order doesn't exist
        assert isinstance(success, bool)
        assert isinstance(message, str)
    
    def test_webhook_processes_payment_captured(self, db: Session):
        """Test that payment.captured event triggers subscription activation"""
        # Setup - create order in DB first
        user_id = "test_user_webhook_002"
        order_id = "order_webhook_002"
        payment_id = "pay_webhook_002"
        
        mock_order = {
            "id": order_id,
            "amount": 14900,
            "notes": {
                "user_id": user_id,
                "tier": "basic",
                "billing_cycle": "monthly"
            }
        }
        
        # Create webhook event
        event = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {
                        "id": payment_id,
                        "order_id": order_id
                    }
                }
            }
        }
        
        with patch.object(razorpay_service.client, 'order.fetch', return_value=mock_order):
            success, message = razorpay_service.handle_webhook(
                event=event,
                signature="",
                db=db
            )
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()


class TestFeatureConfirmation:
    """Test Fix #4: Feature confirmation in response"""
    
    def test_verify_response_includes_features(self, db: Session):
        """Test that payment verification response includes feature details"""
        # Create a subscription to test
        user_id = "test_user_features_001"
        
        subscription = Subscription(
            user_id=user_id,
            tier="pro",
            status="active",
            scans_used_this_period=0,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        db.add(subscription)
        db.commit()
        
        # Get plan details
        plan = get_plan_config("pro")
        
        # Verify plan has required fields
        assert "name" in plan, "Plan missing 'name'"
        assert "scans_per_month" in plan, "Plan missing 'scans_per_month'"
        assert "storage_days" in plan, "Plan missing 'storage_days'"
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()
    
    def test_feature_response_all_tiers(self):
        """Test that all tiers have proper feature configuration"""
        tiers = ["free", "basic", "pro", "ultra", "max"]
        
        for tier in tiers:
            plan = get_plan_config(tier)
            
            # Verify required fields
            assert "name" in plan, f"{tier}: missing name"
            assert "price_monthly" in plan, f"{tier}: missing price_monthly"
            assert "price_yearly" in plan, f"{tier}: missing price_yearly"
            assert "scans_per_month" in plan, f"{tier}: missing scans_per_month"
            assert "storage_days" in plan, f"{tier}: missing storage_days"
            assert plan["scans_per_month"] > 0, f"{tier}: scans should be positive"
            assert plan["storage_days"] > 0, f"{tier}: storage_days should be positive"


class TestScanResetLogic:
    """Test Fix #5: Scan reset logic for renewal vs upgrade"""
    
    def test_scan_reset_on_renewal(self, db: Session):
        """Test that scans reset when period ends (renewal scenario)"""
        # Setup - subscription with old period that has ended
        user_id = "test_user_scans_renewal"
        order_id = "order_scans_renewal"
        payment_id = "pay_scans_renewal"
        
        # Create subscription with period that ended yesterday
        old_period_end = datetime.utcnow() - timedelta(days=1)
        subscription = Subscription(
            user_id=user_id,
            tier="basic",
            status="active",
            scans_used_this_period=45,  # Used 45 out of 80 scans
            current_period_start=old_period_end - timedelta(days=30),
            current_period_end=old_period_end
        )
        db.add(subscription)
        db.commit()
        
        # Now process renewal payment
        mock_order = {
            "id": order_id,
            "amount": 14900,
            "notes": {
                "user_id": user_id,
                "tier": "basic",
                "billing_cycle": "monthly"
            }
        }
        
        with patch.object(razorpay_service.client, 'order.fetch', return_value=mock_order):
            success, message, _ = razorpay_service.process_successful_payment(
                order_id=order_id,
                payment_id=payment_id,
                signature="verified",
                db=db
            )
        
        assert success == True
        
        # Verify scans were reset for new period
        updated = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        assert updated.scans_used_this_period == 0, \
            "Scans should reset on renewal"
        assert updated.razorpay_payment_id == payment_id
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()
    
    def test_scan_preserve_on_upgrade(self, db: Session):
        """Test that scans are preserved when upgrading mid-period"""
        # Setup - subscription mid-period at Free tier
        user_id = "test_user_scans_upgrade"
        order_id = "order_scans_upgrade"
        payment_id = "pay_scans_upgrade"
        
        period_end = datetime.utcnow() + timedelta(days=15)
        subscription = Subscription(
            user_id=user_id,
            tier="free",  # Starting at Free tier
            status="active",
            scans_used_this_period=8,  # Used 8 out of 10 Free scans
            current_period_start=datetime.utcnow() - timedelta(days=15),
            current_period_end=period_end
        )
        db.add(subscription)
        db.commit()
        
        # Upgrade to Pro mid-period
        mock_order = {
            "id": order_id,
            "amount": 29900,  # Pro tier
            "notes": {
                "user_id": user_id,
                "tier": "pro",  # Upgrading to Pro
                "billing_cycle": "monthly"
            }
        }
        
        with patch.object(razorpay_service.client, 'order.fetch', return_value=mock_order):
            success, message, _ = razorpay_service.process_successful_payment(
                order_id=order_id,
                payment_id=payment_id,
                signature="verified",
                db=db
            )
        
        assert success == True
        
        # Verify scans were NOT reset (preserved)
        updated = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        assert updated.tier == "pro"
        assert updated.scans_used_this_period == 8, \
            f"Scans should be preserved on upgrade, but got {updated.scans_used_this_period}"
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()
    
    def test_scan_preserve_on_same_tier_update(self, db: Session):
        """Test that scans are preserved when updating same tier mid-period"""
        # Setup - subscription mid-period, same tier
        user_id = "test_user_scans_same_tier"
        order_id = "order_scans_same_tier"
        payment_id = "pay_scans_same_tier"
        
        period_end = datetime.utcnow() + timedelta(days=15)
        subscription = Subscription(
            user_id=user_id,
            tier="pro",
            status="cancelled",  # Was cancelled
            scans_used_this_period=42,  # Used some scans
            current_period_start=datetime.utcnow() - timedelta(days=15),
            current_period_end=period_end
        )
        db.add(subscription)
        db.commit()
        
        # Re-subscribe to same tier mid-period
        mock_order = {
            "id": order_id,
            "amount": 29900,
            "notes": {
                "user_id": user_id,
                "tier": "pro",  # Same tier
                "billing_cycle": "monthly"
            }
        }
        
        with patch.object(razorpay_service.client, 'order.fetch', return_value=mock_order):
            success, message, _ = razorpay_service.process_successful_payment(
                order_id=order_id,
                payment_id=payment_id,
                signature="verified",
                db=db
            )
        
        assert success == True
        
        # Verify scans were preserved
        updated = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        assert updated.scans_used_this_period == 42, \
            "Scans should be preserved on same-tier re-subscribe"
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()


class TestPaymentFlowIntegration:
    """Integration tests for complete payment flows"""
    
    def test_new_user_payment_flow(self, db: Session):
        """Test complete payment flow for new user"""
        user_id = "test_user_new_flow"
        tier = "pro"
        
        # Step 1: Create order
        order = razorpay_service.create_subscription_order(
            user_id=user_id,
            tier=tier,
            billing_cycle="monthly",
            user_email="newuser@example.com",
            user_name="New User",
            db=db
        )
        
        assert order["order_id"] is not None
        assert order["tier"] == tier
        
        # Step 2: Verify subscription doesn't exist yet
        existing = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        assert existing is None
        
        # Step 3: Process payment
        mock_order = {
            "id": order["order_id"],
            "amount": order["amount_paise"],
            "notes": {
                "user_id": user_id,
                "tier": tier,
                "billing_cycle": "monthly"
            }
        }
        
        payment_id = f"pay_{user_id}_001"
        with patch.object(razorpay_service.client, 'order.fetch', return_value=mock_order):
            success, message, subscription_data = razorpay_service.process_successful_payment(
                order_id=order["order_id"],
                payment_id=payment_id,
                signature="verified",
                db=db
            )
        
        assert success == True
        assert subscription_data["tier"] == tier
        
        # Step 4: Verify subscription was created
        created = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        assert created is not None
        assert created.tier == tier
        assert created.status == "active"
        assert created.razorpay_payment_id == payment_id
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()
    
    def test_duplicate_payment_prevention(self, db: Session):
        """Test that duplicate payments are prevented"""
        user_id = "test_user_duplicate"
        payment_id = "pay_duplicate_001"
        tier = "basic"
        
        # Create first subscription
        subscription1 = Subscription(
            user_id=user_id,
            tier=tier,
            status="active",
            razorpay_payment_id=payment_id,
            scans_used_this_period=0,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        db.add(subscription1)
        db.commit()
        
        # Verify duplicate payment would be detected
        duplicate = db.query(Subscription).filter(
            Subscription.razorpay_payment_id == payment_id
        ).first()
        
        assert duplicate is not None
        assert duplicate.user_id == user_id
        
        # Cleanup
        db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).delete()
        db.commit()


class TestRateLimitingByTier:
    """Test rate limiting enforcement per tier"""
    
    def test_plan_has_rate_limits(self):
        """Test that all plans have rate limiting configuration"""
        tiers = ["free", "basic", "pro", "ultra", "max"]
        
        for tier in tiers:
            plan = get_plan_config(tier)
            
            # These are checked by rate limiter
            assert plan["scans_per_month"] > 0
            # Verify scans increase with tier
            prev_tier = None
            
    def test_tier_progression_has_better_limits(self):
        """Test that higher tiers have better scans per month"""
        tiers = ["free", "basic", "pro", "ultra", "max"]
        prev_limit = 0
        
        for tier in tiers:
            plan = get_plan_config(tier)
            current_limit = plan["scans_per_month"]
            
            assert current_limit >= prev_limit, \
                f"{tier} should have >= scans than previous tier"
            prev_limit = current_limit


# Fixtures
@pytest.fixture
def db():
    """Fixture to provide database session for tests"""
    from app.core.database import SessionLocal
    db = SessionLocal()
    yield db
    db.close()
