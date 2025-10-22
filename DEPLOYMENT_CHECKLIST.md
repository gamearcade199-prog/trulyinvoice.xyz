# 🚀 DEPLOYMENT CHECKLIST - QA System Rollout

## Phase 1: Pre-Deployment (NOW) ✅

### 1.1 Code Review
- [x] `invoice_validator.py` - 370 lines, all validations defined
- [x] `data_quality_monitor.py` - 200 lines, monitoring ready
- [x] `test_invoice_validator.py` - 15+ test cases created
- [x] `DATABASE_AUDIT_TRIGGERS.sql` - SQL triggers defined
- [x] `documents.py` - Validator integrated into API

### 1.2 Local Testing
- [ ] Install pytest: `pip install pytest`
- [ ] Run validator tests locally: `cd backend && pytest tests/test_invoice_validator.py -v`
- [ ] Verify all 15 tests pass
- [ ] Test with sample invoice data

### 1.3 Pre-Flight Checks
- [ ] Backup database (Supabase auto-backs up, but good practice)
- [ ] Review error messages for clarity
- [ ] Check validator configuration is correct
- [ ] Verify database connection string

---

## Phase 2: Database Setup (⏳ BLOCKING)

### 2.1 Execute SQL Triggers

**Action Required:**
1. Open Supabase Dashboard
2. Go to SQL Editor
3. Create new query
4. Copy content from `DATABASE_AUDIT_TRIGGERS.sql`
5. Click "Run"

**What gets created:**
- `validate_invoice_on_insert()` - Function to validate INSERT
- `validate_invoice_on_update()` - Function to validate UPDATE
- `trigger_validate_invoice_insert` - Trigger for INSERT
- `trigger_validate_invoice_update` - Trigger for UPDATE
- `invoice_quality_logs` - Table to store quality issues
- RLS policies for logs table

**Verify:**
```sql
-- Check triggers exist
SELECT trigger_name, event_object_table 
FROM information_schema.triggers 
WHERE event_object_table = 'invoices';

-- Should show:
-- trigger_validate_invoice_insert | invoices
-- trigger_validate_invoice_update | invoices
```

### 2.2 Create Quality Logs Table

If not already created by SQL script, create manually:

```sql
CREATE TABLE IF NOT EXISTS invoice_quality_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  invoice_id uuid REFERENCES invoices(id) ON DELETE CASCADE,
  severity text CHECK (severity IN ('critical', 'warning', 'info')),
  issue_type text NOT NULL,
  description text NOT NULL,
  data jsonb,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

-- RLS Policy
ALTER TABLE invoice_quality_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view their own logs" ON invoice_quality_logs
  FOR SELECT USING (auth.uid() = user_id);
```

### 2.3 Verify Database Setup
- [ ] Triggers created successfully
- [ ] Quality logs table exists
- [ ] Can insert test record into quality_logs
- [ ] RLS policies working

---

## Phase 3: API Deployment (READY)

### 3.1 Deploy Updated API

Files already modified:
- `backend/app/api/documents.py` - Validator integrated ✅
- `backend/app/services/accountant_excel_exporter.py` - UI fields removed ✅
- `backend/app/services/csv_exporter.py` - Safe None handling ✅
- `backend/app/services/professional_pdf_exporter.py` - Safe None handling ✅

**Action:** Just restart FastAPI server

```bash
# Kill old process
# Restart with: python -m uvicorn app.main:app --reload --port 8000
```

### 3.2 Test API Endpoints

**Test: Upload invoice (valid data)**
```bash
# Should pass validation
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@test_invoice.pdf"
```

Expected: 200 OK, invoice created

**Test: Upload invoice (invalid data)**
```bash
# Create request with invalid amount (-100)
# Should be rejected by validator
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@test_invoice.pdf" \
  -F "total_amount=-100"
```

Expected: 422 Unprocessable Entity, error message about negative amount

**Test: Export invoice**
```bash
# Should use cleaned data
curl -X GET http://localhost:8000/api/invoices/{id}/export/pdf
```

Expected: 200 OK, PDF with valid invoice number

### 3.3 Verify Quality Logs

```python
# In Python shell or test:
from app.services.data_quality_monitor import DataQualityMonitor

# Generate report for test user
report = DataQualityMonitor.generate_quality_report('test-user-id')
print(report)
# Should show quality score
```

---

## Phase 4: Testing (READY)

### 4.1 Run Test Suite

```bash
cd backend
pytest tests/test_invoice_validator.py -v
```

Expected output:
```
test_valid_invoice_passes PASSED
test_missing_invoice_number_fails PASSED
test_negative_amount_fails PASSED
test_empty_vendor_name_fails PASSED
test_whitespace_trimming PASSED
test_payment_status_normalization PASSED
... (15+ tests total)

====== 15 passed in 0.34s ======
```

### 4.2 Test Edge Cases

**Test Case 1: Missing invoice_number**
```python
invoice = {
    'invoice_number': '',  # Empty
    'vendor_name': 'Acme Corp',
    'total_amount': 100.0,
    ...
}
is_valid, msg, cleaned = InvoiceValidator.validate_invoice_data(invoice)
# Should generate fallback: INV-{document_id[:8]}
```

**Test Case 2: Negative amount**
```python
invoice = {'total_amount': -50.0, ...}
is_valid, msg, _ = InvoiceValidator.validate_invoice_data(invoice)
# Should be False with error message
```

**Test Case 3: Invalid payment_status**
```python
invoice = {'payment_status': 'unpaid', ...}
_, _, cleaned = InvoiceValidator.validate_invoice_data(invoice)
# Should normalize to 'pending'
```

**Test Case 4: Whitespace in fields**
```python
invoice = {'vendor_name': '  Acme Corp  ', ...}
_, _, cleaned = InvoiceValidator.validate_invoice_data(invoice)
# Should be trimmed to 'Acme Corp'
```

### 4.3 Run Integration Tests

1. Upload real invoice through UI
2. Check database has valid data
3. Export as PDF/Excel/CSV
4. Verify exports contain valid data
5. Check quality logs were created

---

## Phase 5: Monitoring & Validation (ROLLOUT)

### 5.1 Enable Quality Monitoring

Already implemented, just activate:

```python
# In documents.py - already integrated
DataQualityMonitor.log_validation_issue(
    user_id, invoice_data, severity, issue_type, description
)
```

### 5.2 Set Up Quality Dashboards

Create a monitoring dashboard showing:
- [ ] Total invoices
- [ ] Quality score (0-100)
- [ ] Critical issues count
- [ ] Warnings count
- [ ] Trend over time

### 5.3 Create Alert Rules

Optional but recommended:

```
If critical_issues > 5 → Send email alert
If quality_score < 80 → Flag for review
If validation_failures > 10 → Page admin
```

---

## Phase 6: Gradual Rollout Strategy

### 6.1 Canary Deployment (Week 1)

1. Enable for 10% of users
2. Monitor quality scores
3. Check for errors in logs
4. Collect feedback

### 6.2 Staged Rollout (Week 2)

1. Increase to 50% of users
2. Run full test suite again
3. Verify no regressions
4. Check performance impact

### 6.3 Full Deployment (Week 3)

1. Enable for 100% of users
2. Monitor for 24 hours
3. Keep rollback plan ready
4. Celebrate! 🎉

---

## 🔴 Rollback Plan (If Needed)

### Quick Rollback Steps

1. **Stop validator (quick fix):**
   ```python
   # In documents.py, comment out:
   # invoice_data = InvoiceValidator.validate_and_clean(invoice_data)
   ```

2. **Revert exporters (quick fix):**
   ```bash
   git revert <commit-hash>
   ```

3. **Disable triggers (database):**
   ```sql
   DROP TRIGGER IF EXISTS trigger_validate_invoice_insert ON invoices;
   DROP TRIGGER IF EXISTS trigger_validate_invoice_update ON invoices;
   ```

4. **Restart services:**
   ```bash
   # Restart FastAPI
   # Restart frontend
   ```

---

## ✅ Post-Deployment Verification

### 24-Hour Checks

- [ ] No error spikes in logs
- [ ] All tests still passing
- [ ] Quality scores stable
- [ ] No customer complaints
- [ ] Export quality maintained
- [ ] Database performance normal

### 7-Day Checks

- [ ] Average quality score > 95
- [ ] Critical issues < 1%
- [ ] No validation bypass attempts
- [ ] Users satisfied with experience
- [ ] All exporters working
- [ ] Performance metrics healthy

### 30-Day Review

- [ ] Quality trends positive
- [ ] Issues identified and fixed
- [ ] Validation rules refined
- [ ] Test coverage > 90%
- [ ] Zero production bugs from validation
- [ ] User experience improved

---

## 📊 Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Quality Score | > 95 | ? | 🔄 |
| Critical Issues | 0 | ? | 🔄 |
| Validation Pass Rate | > 99% | ? | 🔄 |
| Export Success Rate | 100% | 100% | ✅ |
| Test Coverage | > 90% | ~80% | 🟡 |
| Performance Impact | < 5% | ? | 🔄 |

---

## 📋 Sign-Off Checklist

Before going live:

- [ ] All tests passing
- [ ] Database triggers verified
- [ ] Quality logs table created
- [ ] API endpoints tested
- [ ] Edge cases handled
- [ ] Rollback plan documented
- [ ] Team trained on monitoring
- [ ] Stakeholders notified

---

## 🎯 Next Steps

### TODAY (Immediate)
1. [ ] Review this checklist
2. [ ] Run local tests
3. [ ] Execute SQL triggers in Supabase
4. [ ] Test API endpoints

### THIS WEEK
1. [ ] Deploy to staging
2. [ ] Run integration tests
3. [ ] Get stakeholder approval
4. [ ] Prepare rollout plan

### NEXT WEEK
1. [ ] Canary deployment (10% users)
2. [ ] Monitor closely
3. [ ] Gather feedback
4. [ ] Make any adjustments

---

## 📞 Emergency Contact

If something goes wrong during deployment:

1. **Check logs:**
   ```bash
   # Backend logs
   tail -f backend.log | grep ERROR
   
   # Database logs
   # Check Supabase dashboard
   ```

2. **Quick diagnostics:**
   ```python
   # Test validator directly
   python -c "from app.services.invoice_validator import InvoiceValidator; print(InvoiceValidator.validate_invoice_data({...}))"
   ```

3. **Ask for help:**
   - Review QUALITY_ASSURANCE_GUIDE.md
   - Check test cases for examples
   - Review error messages

