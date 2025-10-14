# 🔍 Database Structure Audit & Fix Guide

## The Problem You're Facing

Your error shows:
```
ERROR: cannot alter type of a column used by a view or rule
DETAIL: rule _RETURN on view gst_invoices depends on column "place_of_supply"
```

This means:
1. ✅ Your database has views (like `gst_invoices`) that use certain columns
2. ❌ You can't alter those columns without first dropping the views
3. ✅ The solution: Drop views → Alter columns → Recreate views

---

## 📊 Step 1: Audit Your Current Database

Run this to see what's in your database:

### In Supabase Dashboard → SQL Editor:
```sql
-- Copy and paste the entire contents of AUDIT_DATABASE_STRUCTURE.sql
```

This will show you:
- ✅ All columns in the `invoices` table
- ⚠️ Which columns are too short (VARCHAR ≤ 10)
- 📊 All views that exist
- 🔗 All indexes and constraints
- 📈 Sample data with field lengths

---

## 🔧 Step 2: Fix the Database Schema

After you see the audit results, run this:

### In Supabase Dashboard → SQL Editor:
```sql
-- Copy and paste the entire contents of FIX_VARCHAR_WITH_VIEWS.sql
```

This script will:
1. ✅ **Drop all views** (gst_invoices, invoice_essentials, overdue_invoices, monthly_invoice_summary)
2. ✅ **Alter column types**:
   - `currency`: VARCHAR(10) → VARCHAR(50)
   - `vendor_pan`: VARCHAR(10) → VARCHAR(50)
   - `vendor_tan`: VARCHAR(10) → VARCHAR(50)
   - `vendor_pincode`: VARCHAR(10) → VARCHAR(20)
   - `place_of_supply`: VARCHAR(10) → VARCHAR(100)
   - `payment_status`: VARCHAR(10) → VARCHAR(50)
   - `payment_method`: VARCHAR(10) → VARCHAR(50)
3. ✅ **Recreate all views** with the exact same structure

---

## ✅ Step 3: Test Your Invoice Upload

After running the fix:

1. **Upload your invoice** (tax.pdf) again
2. You should see:
   ```
   ✅ AI extracted: Facebook India Online Services Pvt. Ltd. - ₹1,895.68
   💾 Creating invoice for user...
   ✅ Successfully saved invoice!
   INFO: 127.0.0.1:62924 - "POST /api/documents/.../process HTTP/1.1" 200 OK
   ```

---

## 📋 What Your Database Should Have

Based on your backend code, your `invoices` table needs these columns:

### Core Fields ✅
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `document_id` (UUID, Foreign Key)
- `category_id` (UUID, nullable)

### Vendor Information ✅
- `vendor_name` (VARCHAR, required)
- `vendor_gstin` (VARCHAR(15))
- `vendor_pan` (VARCHAR(50)) ← **Should be 50, not 10**
- `vendor_tan` (VARCHAR(50)) ← **Should be 50, not 10**
- `vendor_email` (VARCHAR)
- `vendor_phone` (VARCHAR)
- `vendor_address` (TEXT)
- `vendor_pincode` (VARCHAR(20)) ← **Should be 20, not 10**

### Invoice Details ✅
- `invoice_number` (VARCHAR, required)
- `invoice_date` (DATE, required)
- `due_date` (DATE)
- `po_number` (VARCHAR)
- `invoice_type` (VARCHAR)

### GST & Tax Fields ✅
- `subtotal` (DECIMAL)
- `cgst` (DECIMAL)
- `sgst` (DECIMAL)
- `igst` (DECIMAL)
- `cess` (DECIMAL)
- `total_gst` (DECIMAL)
- `place_of_supply` (VARCHAR(100)) ← **Should be 100, not 10**
- `hsn_code` (VARCHAR)
- `sac_code` (VARCHAR)
- `reverse_charge` (BOOLEAN)

### Other Taxes ✅
- `vat` (DECIMAL)
- `service_tax` (DECIMAL)
- `tds_amount` (DECIMAL)
- `tds_percentage` (DECIMAL)
- `tcs_amount` (DECIMAL)

### Charges ✅
- `discount` (DECIMAL)
- `discount_percentage` (DECIMAL)
- `shipping_charges` (DECIMAL)
- `freight_charges` (DECIMAL)
- `handling_charges` (DECIMAL)
- `packing_charges` (DECIMAL)
- `insurance_charges` (DECIMAL)
- `loading_charges` (DECIMAL)
- `other_charges` (DECIMAL)
- `roundoff` (DECIMAL)
- `advance_paid` (DECIMAL)

### Amounts ✅
- `total_amount` (DECIMAL, required)
- `currency` (VARCHAR(50)) ← **Should be 50, not 10**
- `exchange_rate` (DECIMAL)

### Payment ✅
- `payment_status` (VARCHAR(50)) ← **Should be 50, not 10**
- `payment_method` (VARCHAR(50)) ← **Should be 50, not 10**
- `payment_date` (DATE)
- `payment_terms` (TEXT)
- `bank_name` (VARCHAR)
- `account_number` (VARCHAR)
- `ifsc_code` (VARCHAR)
- `upi_id` (VARCHAR)

### Classification ✅
- `business_type` (VARCHAR)
- `supply_type` (VARCHAR)
- `transaction_type` (VARCHAR)

### Data Storage ✅
- `line_items` (JSONB) ← **For storing invoice line items**
- `raw_extracted_data` (JSONB) ← **For storing raw AI output**

### Metadata ✅
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

---

## 🎯 Is Your Schema Perfect?

### ✅ What's Good:
- You have all the required columns for Indian invoices
- GST fields are properly structured
- Line items storage (JSONB)
- Views for quick queries

### ⚠️ What Needs Fixing:
- **Column sizes are too small** (VARCHAR(10) → should be VARCHAR(50-100))
- This is causing your upload error

### 🚀 After the Fix:
Your schema will be **perfect** for:
- ✅ Indian GST invoices
- ✅ International invoices
- ✅ Complex line items
- ✅ All payment methods
- ✅ All Indian states (place_of_supply)
- ✅ Any currency name

---

## 📊 Database Health Check

After running the audit script, look for:

### Red Flags 🚩
- Any column with `character_maximum_length <= 10` (except codes like PAN/GSTIN)
- Missing views after the fix
- Missing indexes on frequently queried columns

### Green Flags ✅
- `currency` is VARCHAR(50)
- `place_of_supply` is VARCHAR(100)
- `payment_status` is VARCHAR(50)
- `payment_method` is VARCHAR(50)
- All views exist (gst_invoices, invoice_essentials, etc.)
- Indexes on user_id, invoice_date, payment_status

---

## 🎯 Quick Commands

### 1. Audit Database:
```bash
# In Supabase Dashboard → SQL Editor
# Run: AUDIT_DATABASE_STRUCTURE.sql
```

### 2. Fix Database:
```bash
# In Supabase Dashboard → SQL Editor
# Run: FIX_VARCHAR_WITH_VIEWS.sql
```

### 3. Test Upload:
```bash
# In your terminal
cd backend
start-backend.bat

# In another terminal
cd frontend
npm run dev

# Upload invoice at: http://localhost:3000/upload
```

---

## 🎊 Expected Result

After the fix, when you upload `tax.pdf`:

```
📄 Processing: tax.pdf for user d1949c37-d380-46f4-ad30-20ae84aff1ad
  ⬇️ Downloading from: https://ldvwxqluaheuhbycdpwn.supabase.co/storage/v...
  📄 PDF detected - extracting text...
  🤖 Extracted 1280 chars - sending to AI...
📋 Extracted 2 line items from invoice
💰 Tax breakdown extracted: {'subtotal': 1606.51, 'igst': 289.17, 'total_amount': 1895.68}
  ✅ AI extracted: Facebook India Online Services Pvt. Ltd. - ₹1,895.68
  💾 Creating invoice for user...
  ✅ Successfully saved invoice with ID: abc-123-def
INFO: 127.0.0.1:62924 - "POST /api/documents/.../process HTTP/1.1" 200 OK
```

**Status Code: 200 ✅** (not 500 ❌)

---

## 📝 Files Created

1. **`AUDIT_DATABASE_STRUCTURE.sql`** - Run this first to see what's wrong
2. **`FIX_VARCHAR_WITH_VIEWS.sql`** - Run this second to fix everything
3. **`DATABASE_AUDIT_AND_FIX_GUIDE.md`** - This guide

---

## 💡 Pro Tips

### Tip 1: Always Audit First
Run the audit script before making changes to see exactly what's wrong.

### Tip 2: Backup Before Fixing
Supabase automatically backs up your data, but you can also:
```sql
-- Export your data first
SELECT * FROM invoices;
```

### Tip 3: Check After Fixing
After running the fix, verify with:
```sql
SELECT column_name, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'invoices'
  AND column_name IN ('currency', 'place_of_supply', 'payment_status')
ORDER BY column_name;
```

You should see:
- currency: 50
- payment_status: 50
- place_of_supply: 100

---

## ❓ FAQ

### Q: Will this delete my existing invoices?
**A:** No! This only changes column types, not data.

### Q: What if the script fails?
**A:** Supabase has automatic backups. You can also rollback by closing the SQL editor without committing.

### Q: Do I need to restart my backend?
**A:** No, the backend will work immediately after the database fix.

### Q: What if I have custom views?
**A:** The audit script will show all your views. Add them to the fix script before running.

---

**Status:** Ready to audit and fix! 🚀

Run the audit script first to see exactly what needs fixing!
