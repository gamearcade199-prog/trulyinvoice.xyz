# 🎯 EXPORT & AI EXTRACTION - Quick Guide

## ✅ **NEW FEATURE: Export to Excel!**

### How to Export Your Invoices
1. Go to: http://localhost:3000/invoices
2. Click: **Blue "Export" button** (top right)
3. File downloads: `invoices_2025-10-12.csv`
4. Open in **Excel** or **Google Sheets**

### What You Get in Export:
- Invoice Number
- Vendor Name  
- Invoice Date
- Due Date
- Subtotal
- Tax Amount (GST)
- Total Amount
- Payment Status
- Payment Method
- GSTIN
- Created Date

### Using Exported Data:
- **Excel Analysis**: Pivot tables, charts, formulas
- **Import to QuickBooks**: CSV import
- **Import to Tally**: CSV import  
- **Email Reports**: Attach CSV to email
- **Google Sheets**: Upload and share

---

## ⚠️ Why Your Invoice Shows "Processing..."

**The Problem:**
- You uploaded BEFORE backend was ready
- AI extraction never ran
- File is in storage, but no extracted data

**The Solution: RE-UPLOAD (30 seconds)**

### Quick Fix:
```
1. Click trash icon → Delete "Processing..." invoice
2. Go to Upload page
3. Upload SAME PDF again
4. Watch backend terminal for logs:
   ✅ "Starting processing for document..."
   ✅ "Extracting data..."
   ✅ "Extraction successful..."
5. Wait 10-15 seconds
6. Refresh invoices page
7. ✅ Real data appears!
```

---

## 🔍 What to Watch During Upload

### Backend Terminal (Should Show):
```
2025-10-12 - INFO - Starting processing for document 2
2025-10-12 - INFO - Downloading file from storage: user_id/filename.pdf
2025-10-12 - INFO - Extracting data from C:\Users\...\tmp123.pdf
2025-10-12 - INFO - Extraction successful. Confidence: 0.95
2025-10-12 - INFO - Created new invoice for document 2
```

### Browser Console (F12 → Console):
```
✅ AI extraction completed for document: 2
{
  vendor_name: "ABC Company",
  total_amount: 15000,
  tax_amount: 2700,
  ...
}
```

### Invoices Page (After Refresh):
```
✅ Vendor: ABC Company (not "Processing...")
✅ Amount: ₹15,000 (not ₹0)
✅ GST: ₹2,700 (not ₹0)
✅ Date: 2025-09-01 (not N/A)
✅ Status: Unpaid (not "Processing")
```

---

## 📊 COMPLETE WORKFLOW

### 1. Upload Invoice
- Drag & drop PDF
- Click "Process Invoice"
- File saves to Supabase Storage

### 2. AI Extraction (Automatic)
- Backend calls Google Cloud Vision API
- Extracts text from PDF
- OpenAI GPT-4o structures the data
- Calculates GST (CGST + SGST + IGST)
- Saves to database

### 3. View Invoice
- See all extracted data
- Click eye icon to view original PDF
- Edit if needed (coming soon)

### 4. Export Data
- Click Export button
- Download CSV
- Open in Excel
- Analyze/share/import

---

## 🐛 TROUBLESHOOTING

### "Processing..." Won't Change
**Cause**: AI extraction never ran  
**Fix**: Delete and re-upload

### Export Button Not Working  
**Cause**: Missing invoiceUtils import
**Fix**: Already fixed! Just refresh page

### View Button Shows Error
**Cause**: storage_path missing
**Fix**: Re-upload file

### ₹0 Amounts After Re-upload
**Cause**: Backend error or invalid PDF
**Check Backend Logs For**:
- API key errors
- File format issues
- AI extraction failures

---

## 💡 PRO TIPS

1. **Watch Backend Logs**: See AI extraction in real-time
2. **Use Browser Console**: Debug any issues (F12)
3. **Export Regularly**: Backup your data
4. **Check Confidence Score**: >0.7 is good, <0.5 needs review

---

## ✅ CURRENT STATUS

**✅ Working:**
- Export to CSV/Excel
- View PDFs (signed URLs)
- Delete invoices
- Upload new invoices
- AI extraction (when backend is running)

**⚠️ Needs Action:**
- Re-upload your "Processing..." invoice
- Test the AI extraction end-to-end

**🎯 Next Steps:**
1. Delete old invoice
2. Re-upload same PDF
3. Verify real data appears
4. Export to Excel
5. Done! 🎉

---

**Backend is running! Just re-upload your PDF to see the AI magic! 🚀**
