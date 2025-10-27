# ⚡ TESTING QUICK START GUIDE
**Fast Reference: What Tests to Run & How to Set Them Up**

---

## 📌 ONE-PAGE SUMMARY

### Current State
- ✅ Build: Passing
- ✅ Build Warnings: 0
- ⚠️ Tests: 26/415 (6%)
- ⚠️ Coverage: ~23%
- 🔴 Production Ready: NO

### To Launch Successfully
```
Need 250+ tests covering:
✓ 80%+ critical paths
✓ All API endpoints
✓ Payment security
✓ User data protection
✓ Export functionality
✓ Subscription system
```

**Timeline:** 3-4 weeks to 250 tests

---

## 🎯 PRIORITY 1: CRITICAL TESTS (Week 1-2)

### Setup (30 min)
```bash
# Backend
cd backend
pip install pytest pytest-cov pytest-asyncio httpx testcontainers

# Frontend  
cd frontend
npm install --save-dev jest @testing-library/react @testing-library/jest-dom cypress
```

### Must-Have Tests (This Week)

#### 1. Payment Processing (12 tests)
```python
# backend/tests/test_payments.py
- Payment order creation
- Razorpay signature verification
- Duplicate payment detection
- Amount validation
- Subscription tier activation
- Payment status updates
```
**Why:** Payment failures = lost revenue

#### 2. Authentication (15 tests)
```python
# backend/tests/test_auth.py
- User registration
- JWT token generation
- Token validation
- Session management
- Password hashing
- Multi-user isolation
```
**Why:** Auth breach = data breach

#### 3. Invoice Upload (10 tests)
```python
# backend/tests/test_invoice_upload.py
- File validation
- AI extraction
- Data parsing
- Format detection
- Error handling
```
**Why:** Core product feature

#### 4. Data Protection (8 tests)
```python
# backend/tests/test_rls.py
- User isolation (RLS)
- Admin capabilities
- Public/private access
- Subscription limits
```
**Why:** GDPR/compliance critical

---

## 🎯 PRIORITY 2: IMPORTANT TESTS (Week 2-3)

#### 5. Export Formats (15 tests)
```python
# backend/tests/test_exports.py
- CSV generation
- Excel formatting
- PDF rendering
- Special character handling
- Large file export
```

#### 6. API Endpoints (20 tests)
```python
# backend/tests/test_api.py
- GET /api/invoices
- POST /api/invoices
- PUT /api/invoices/{id}
- DELETE /api/invoices/{id}
- Rate limiting
```

#### 7. Component Tests (15 tests)
```tsx
// frontend/__tests__/UploadZone.test.tsx
- File drag-drop
- Format validation
- Error messages
- Loading states

// frontend/__tests__/RazorpayCheckout.test.tsx
- Payment button
- Modal display
- Error handling
```

#### 8. E2E Flows (10 tests)
```bash
# Cypress - Real user scenarios
- Signup → Upload → Export
- Upgrade subscription
- Change settings
```

---

## 📊 TEST STRUCTURE

### Backend Testing Pattern
```python
# tests/test_module.py
import pytest
from app.services.invoice_validator import InvoiceValidator

class TestInvoiceValidator:
    
    @pytest.fixture
    def valid_invoice(self):
        return {
            'user_id': 'test-user',
            'invoice_number': 'INV-001',
            'vendor_name': 'Test Corp',
            'total_amount': 1000.00,
            'invoice_date': '2025-10-27'
        }
    
    def test_valid_invoice(self, valid_invoice):
        is_valid, msg, data = InvoiceValidator.validate_invoice_data(valid_invoice)
        assert is_valid
    
    def test_missing_user_id(self):
        invoice = {...missing user_id...}
        is_valid, msg, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
```

### Frontend Testing Pattern
```tsx
// __tests__/components/UploadZone.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import UploadZone from '@/components/UploadZone';

describe('UploadZone Component', () => {
    
    it('should accept PDF files', () => {
        render(<UploadZone />);
        const input = screen.getByTestId('file-input');
        
        const file = new File(['content'], 'invoice.pdf', 
            { type: 'application/pdf' });
        
        fireEvent.change(input, { target: { files: [file] } });
        
        expect(screen.getByText(/processing/i)).toBeInTheDocument();
    });
    
    it('should reject non-PDF files', () => {
        render(<UploadZone />);
        const input = screen.getByTestId('file-input');
        
        const file = new File(['content'], 'doc.txt', 
            { type: 'text/plain' });
        
        fireEvent.change(input, { target: { files: [file] } });
        
        expect(screen.getByText(/PDF required/i)).toBeInTheDocument();
    });
});
```

---

## 🚀 QUICK EXECUTION

### Run All Tests
```bash
# Backend
cd backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend
cd frontend
npm test -- --coverage --watchAll=false

# Both
npm run build  # Verify no build errors
```

### Run Specific Tests
```bash
# One file
pytest tests/test_payments.py -v

# One test
pytest tests/test_payments.py::TestPayments::test_order_creation -v

# With coverage
pytest tests/ --cov=app --cov-report=term-missing
```

### CI/CD GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      
      - name: Install dependencies
        run: pip install -r backend/requirements.txt pytest
      
      - name: Run tests
        run: pytest backend/tests/ -v --cov=app
      
      - name: Check coverage
        run: pytest backend/tests/ --cov=app --cov-fail-under=80
```

---

## 📈 COVERAGE TARGETS

### By Component
| Component | Current | Target |
|-----------|---------|--------|
| Authentication | 30% | 90% |
| Payments | 20% | 95% |
| Invoice Processing | 50% | 90% |
| Exports | 0% | 85% |
| UI Components | 0% | 75% |
| Database/RLS | 10% | 90% |
| **Overall** | **23%** | **80%** |

---

## 🔍 HEALTH CHECK TESTS

### Before Every Deployment
```bash
#!/bin/bash

# 1. Build verification
echo "✓ Building..."
npm run build

# 2. Unit tests
echo "✓ Running unit tests..."
pytest tests/ --tb=short

# 3. Coverage check (80% minimum)
echo "✓ Checking coverage..."
pytest tests/ --cov=app --cov-fail-under=80

# 4. Code quality
echo "✓ Linting..."
pylint app/
eslint frontend/src/

# 5. Security check
echo "✓ Security scan..."
bandit -r app/

echo "✅ All checks passed - Ready to deploy!"
```

---

## 📋 WEEKLY CHECKLIST

### Monday
- [ ] Run full test suite
- [ ] Check code coverage
- [ ] Review failed tests
- [ ] Update test plan

### Wednesday  
- [ ] Add tests for new features
- [ ] Fix any failing tests
- [ ] Code review with team
- [ ] Performance check

### Friday
- [ ] Run full E2E tests
- [ ] Security audit
- [ ] Deploy to staging
- [ ] Manual testing
- [ ] Ready for production?

---

## 🎓 TEST PRIORITY BY RISK

### CRITICAL (Do First)
```
1. Payment processing    → Lost $$ if broken
2. User authentication   → Data breach if broken
3. RLS policies         → Data leak if broken
4. Invoice upload       → Core feature broken
```

### HIGH (Do Soon)
```
5. Export functionality → User can't get data
6. Subscription system  → Revenue impact
7. API endpoints        → Service down
```

### MEDIUM (Do Next)
```
8. UI components        → User experience
9. Performance          → Scalability issues
10. Error handling      → User confusion
```

### LOW (Do Later)
```
11. Analytics           → Business intelligence
12. Email notifications → Minor feature
13. Logging            → Debugging aid
```

---

## 💡 TEST WRITING TIPS

### ✅ Good Test
```python
def test_payment_order_prevents_fraud():
    """Verify payment orders include user_id for fraud prevention"""
    order = razorpay_service.create_order(
        user_id='user-1',
        amount=999,
        tier='pro'
    )
    assert order['user_id'] == 'user-1'
    assert order['amount'] == 999
    assert 'signature' in order
```

### ❌ Bad Test
```python
def test_payment():
    """Test payment"""
    order = create_order()
    assert order  # Too vague!
```

### Tips
1. **One assertion per test** (usually)
2. **Clear test names** - says what it tests
3. **Arrange-Act-Assert pattern**
4. **Test edge cases** - not just happy path
5. **Mock external services** - OpenAI, Razorpay, etc.
6. **Use fixtures** - reusable test data
7. **Test error cases** - "what if it fails?"

---

## 🐛 DEBUG FAILED TESTS

```bash
# Verbose output
pytest tests/test_payments.py::test_fraud_detection -vv

# Show print statements
pytest tests/ -s

# Drop into debugger
pytest tests/ --pdb

# Show local variables on failure
pytest tests/ --showlocals

# Run only last failed test
pytest tests/ --lf
```

---

## 📚 USEFUL RESOURCES

### Backend
- pytest docs: https://docs.pytest.org/
- FastAPI testing: https://fastapi.tiangolo.com/advanced/testing-dependencies/
- SQLAlchemy testing: https://docs.sqlalchemy.org/orm/session_basics.html

### Frontend  
- React Testing Library: https://testing-library.com/react
- Cypress: https://docs.cypress.io/
- Jest: https://jestjs.io/

### General
- TDD Best Practices: https://testdriven.io/
- Test Pyramid: https://martinfowler.com/bliki/TestPyramid.html
- Mocking Guide: https://en.wikipedia.org/wiki/Mock_object

---

## 🎯 NEXT 48 HOURS

### Today (2 hours)
- [ ] Read `PRODUCTION_READINESS_COMPLETE_ANALYSIS.md`
- [ ] Set up test infrastructure
- [ ] Run existing tests

### Tomorrow (4 hours)
- [ ] Write 10 payment tests
- [ ] Write 10 auth tests
- [ ] Verify coverage

### By Friday
- [ ] 20+ payment/auth tests passing
- [ ] 50%+ coverage on critical paths
- [ ] CI/CD pipeline working

---

## ✅ LAUNCH READINESS CHECKLIST

Before going to production:

```
Code Quality:
□ 0 build errors
□ 0 build warnings
□ Linting passes
□ Security scan passes (bandit)

Testing:
□ 150+ tests written
□ 80%+ coverage
□ All tests passing
□ E2E tests passing

Performance:
□ API response < 500ms (p95)
□ Export generation < 5 sec
□ Load test: 100 concurrent users

Security:
□ No SQL injection
□ No XSS vulnerabilities
□ RLS policies verified
□ Payment signatures validated

Operations:
□ Error monitoring (Sentry) working
□ Analytics tracking working
□ Database backups automated
□ Logs rotating properly

Documentation:
□ README complete
□ API documentation done
□ Deployment guide written
□ Team trained

Manual Testing:
□ Signup flow works
□ Upload & export works
□ Payment flow works
□ Settings page works
□ Mobile responsive
```

---

**You're ~6% done. Get to 80% and launch! 🚀**
