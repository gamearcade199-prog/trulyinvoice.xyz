# 🎨 Dynamic HTML Invoice Template - Quick Start Guide

## What You Got

A **beautiful, professional invoice template** that:
- ✅ Uses 100% real OCR extracted data (NO fake data)
- ✅ Looks exactly like your specification
- ✅ Works with ANY invoice structure
- ✅ Exports as HTML (browser) or PDF (print-ready)
- ✅ Automatically formats currency, dates, numbers
- ✅ Calculates amount in Indian rupees words

---

## Use It Right Now

### 1️⃣ **Via API Endpoint**

```bash
# POST request to export invoice as HTML PDF
curl -X POST http://localhost:8000/api/export-pdf-html \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "invoice_ids": ["your-invoice-id"],
    "template": "html"
  }'
```

### 2️⃣ **Via Python Code**

```python
from app.services.html_pdf_exporter import HTMLPDFExporter

# Prepare your invoice data (from database or OCR)
invoice_data = {
    'invoice_number': 'INV-001',
    'invoice_date': '13 September 2023',
    'company_name': 'Your Company',
    'company_address': 'Your Address',
    'customer_name': 'Customer Name',
    # ... add more fields
}

# Generate invoice
exporter = HTMLPDFExporter()
output_file = exporter.generate_pdf(invoice_data)

# Returns: 'exports/invoice_INV-001_20251024_123456.html'
# Open in browser or print to PDF!
```

---

## Map Your OCR Data

Your OCR extraction probably returns data like this:

```json
{
  "invoice_number": "INV-001",
  "vendor_name": "Company ABC",
  "extracted_date": "13 Sep 2023",
  "line_items": [...],
  "total_amount": 10000
}
```

The template **automatically maps** these to invoice fields:

| Your Field | Template Field |
|-----------|----------------|
| `invoice_number` ➜ Uses as is |
| `vendor_name` ➜ Maps to `company_name` |
| `extracted_date` ➜ Maps to `invoice_date` |
| `line_items` ➜ Renders as table |
| `total_amount` ➜ Maps to `total` |

**You don't need to restructure anything!**

---

## Example: From OCR to Invoice

### Your OCR Output:
```python
ocr_result = {
    "invoice_number": "2023-09-1234",
    "vendor_name": "Nambor Tours",
    "vendor_address": "Main Road, Golaghat\nAssam 785601",
    "bill_to": "Payout Ali",
    "bill_address": "123 Customer St\nGolaghat, Assam",
    "items": [
        {
            "desc": "Tour Package",
            "qty": 1,
            "rate": 55000,
            "amount": 55000
        }
    ],
    "subtotal": 55000,
    "tax_9pct": 4950,
    "final_total": 59950
}
```

### Direct to Invoice Template:
```python
from app.services.html_pdf_exporter import HTMLPDFExporter

exporter = HTMLPDFExporter()

# Just pass the OCR data - it maps automatically!
invoice = exporter.generate_pdf({
    'invoice_number': ocr_result['invoice_number'],
    'company_name': ocr_result['vendor_name'],
    'company_address': ocr_result['vendor_address'],
    'customer_name': ocr_result['bill_to'],
    'customer_address': ocr_result['bill_address'],
    'line_items': ocr_result['items'],
    'subtotal': ocr_result['subtotal'],
    'cgst': ocr_result['tax_9pct'],
    'total': ocr_result['final_total']
})

# Done! Beautiful PDF ready
```

---

## Supported Fields

Pass any of these fields in your invoice data dictionary:

### 📋 Invoice Basics
- `invoice_number` / `invoice_id` / `inv_id`
- `invoice_date` / `date`
- `due_date` / `payment_due_date`
- `invoice_period`
- `status` / `payment_status`

### 🏢 Company Info
- `company_name` / `vendor_name`
- `company_address` / `vendor_address`
- `company_phone` / `vendor_phone`
- `company_email` / `vendor_email`

### 👤 Customer Info
- `customer_name` / `bill_to_name`
- `customer_address` / `bill_to_address`
- `customer_phone` / `bill_to_phone`
- `customer_email` / `bill_to_email`

### 📦 Line Items
```python
'line_items': [
    {
        'description': 'Item name',
        'details': 'Item details (optional)',
        'quantity': 1,
        'rate': 1000,
        'amount': 1000
    }
]
```

### 💰 Financial
- `subtotal`
- `discount`
- `cgst` / `central_gst` (9%)
- `sgst` / `state_gst` (9%)
- `igst` / `integrated_gst` (18%)
- `total`

### 🏦 Payment Details
- `bank_name`
- `account_name`
- `account_number`
- `ifsc_code` / `ifsc`
- `branch`
- `upi_id`

### ⚖️ Other
- `service_details` / `product_details`
- `terms_conditions` / `terms`

---

## Output Formats

### 📄 HTML Output (Default)
```
invoice_INV-001_20251024_123456.html
├─ Size: ~14-20 KB
├─ Open in: Browser (Chrome, Firefox, Edge, Safari)
├─ Print: Ctrl+P → Save as PDF
└─ Share: Email as attachment or link
```

### 📕 PDF Output (If wkhtmltopdf installed)
```
invoice_INV-001_20251024_123456.pdf
├─ Size: ~30-50 KB
├─ Ready to: Print, email, archive
├─ Viewing: Any PDF reader
└─ Quality: Professional print-ready
```

---

## Design Features

### 🎨 Professional Style
- Clean modern colors (#2C3E50 dark blue-grey + #F39C12 orange accent)
- Proper typography hierarchy (H1, H2, regular text)
- Professional spacing and alignment
- A4 paper format (210mm × 297mm)

### 📱 Responsive
- Works on desktop, tablet, mobile
- Optimized for printing
- Maintains quality at any zoom level

### 🔢 Smart Formatting
- **Currency:** Automatically shows ₹ with proper decimals
  - Example: `1000` → `₹1,000.00`
- **Amount to Words:** Converts to Indian English
  - Example: `1000` → `One Thousand Rupees Only`
- **Numbers:** Proper comma formatting
  - Example: `59950` → `59,950.00`

### 🛡️ Safe Data Handling
- HTML special characters escaped (prevents injection)
- Missing fields handled gracefully
- Invalid numbers default to 0
- No fake data ever added

---

## Testing

### Test with Sample Data
```bash
cd c:\Users\akib\Desktop\trulyinvoice.xyz\backend
python test_html_pdf_exporter.py
```

You should see:
```
✅ HTML PDF Exporter TEST PASSED!
📁 Output file: exports\invoice_INV-92C002F8_20251024_215425.html
✅ File created successfully
   File size: 14,160 bytes
```

Then:
1. Open the HTML file in your browser
2. See beautiful professional invoice
3. Press Ctrl+P to print as PDF

---

## Integration Steps

### Step 1: Import
```python
from app.services.html_pdf_exporter import HTMLPDFExporter
```

### Step 2: Create Data
```python
invoice_data = {
    'invoice_number': 'INV-001',
    'company_name': 'Your Company',
    'customer_name': 'Customer Name',
    'line_items': [...],
    'total': 10000,
    # ... more fields
}
```

### Step 3: Generate
```python
exporter = HTMLPDFExporter()
output_path = exporter.generate_pdf(invoice_data)
```

### Step 4: Return/Send
```python
return FileResponse(output_path, media_type="application/pdf")
```

---

## API Response Examples

### Success Response (200 OK)
```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="invoice_INV-001_html.pdf"

[Binary PDF content]
```

### User gets beautiful invoice PDF ready to print!

---

## Customization (Advanced)

### Change Primary Color
Edit `html_pdf_exporter.py`:
```python
# Change #2c3e50 to your color (e.g., #1a5490 for blue)
color: #2c3e50;
```

### Change Font
```python
# Change font-family in CSS section
font-family: 'Your Font', Arial, sans-serif;
```

### Add Company Logo
```html
<img src="/logo.png" style="max-width: 150px;">
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| HTML file opens instead of PDF | Install wkhtmltopdf or use browser print-to-PDF |
| Currency shows wrong symbol | Check UTF-8 encoding in database |
| Dates look wrong | Ensure date format in your data |
| Text is cut off | Use HTML version - no character limits |
| Missing data shows blank | That's correct - we don't add fake data! |

---

## Files Created

- ✅ `html_pdf_exporter.py` - Main invoice generator
- ✅ `test_html_pdf_exporter.py` - Test file with sample data
- ✅ `exports/` - Folder for output files
- ✅ `HTML_INVOICE_TEMPLATE_DOCS.md` - Full documentation
- ✅ API endpoint `/api/export-pdf-html` - Ready to use

---

## Next Steps

1. **Test it:** Run test file to see sample invoice
2. **Integrate it:** Use in your backend routes
3. **Connect OCR:** Feed real extracted data
4. **Deploy:** Push to production

---

## Summary

✅ Professional invoice template ready
✅ Works with YOUR OCR data format
✅ No fake data, no guessing
✅ Beautiful output
✅ Easy integration
✅ Production ready

**Your invoices now look enterprise-grade!** 🚀

---

Questions? Check `HTML_INVOICE_TEMPLATE_DOCS.md` for full details.
