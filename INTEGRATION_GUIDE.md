# 📊 Integration Guide - Export & Automation

Complete guide to integrate TrulyInvoice with Google Sheets, Zoho, Excel, and other platforms.

---

## 🎯 Quick Overview

| Platform | Method | Difficulty | Setup Time | Best For |
|----------|--------|------------|------------|----------|
| **Excel** | CSV Import | Easy | 1 min | Manual exports |
| **Excel** | Power Query | Medium | 10 min | Auto-refresh from API |
| **Google Sheets** | CSV Import | Easy | 1 min | One-time imports |
| **Google Sheets** | Apps Script | Medium | 15 min | Automated sync |
| **Zoho Books** | CSV Import | Easy | 5 min | Accounting integration |
| **Zapier/Make** | Automation | Easy | 20 min | Multi-app workflows |

---

## 📥 Method 1: Simple CSV Export (Recommended for Beginners)

### Excel - CSV Import
**Best for:** Quick manual exports, one-time data pulls

**Steps:**
1. **Export from TrulyInvoice:**
   - Go to Invoices page
   - Select invoices (or use "Select All")
   - Click "Export Selected" button
   - Download the CSV file

2. **Import to Excel:**
   ```
   Excel → Data tab → Get Data → From File → From Text/CSV
   → Select your downloaded file → Load
   ```

3. **Format as Table:**
   - Select all data
   - Press `Ctrl + T` (Format as Table)
   - Enable filters and sorting

**✅ Pros:** Super easy, no setup  
**❌ Cons:** Manual process, no auto-sync

---

### Google Sheets - CSV Import
**Best for:** Sharing with team, basic collaboration

**Steps:**
1. Export CSV from TrulyInvoice (same as above)
2. Open Google Sheets
3. `File → Import → Upload → Select CSV → Import data`
4. Choose "Replace spreadsheet" or "Append to current sheet"

**✅ Pros:** Cloud-based, shareable  
**❌ Cons:** Still manual, no live updates

---

## 🔄 Method 2: Automated Integration (Advanced)

### Excel - Power Query (Auto-Refresh from API)
**Best for:** Windows users, automated dashboards, scheduled refreshes

**Prerequisites:**
- Excel 2016+ (Windows)
- Your Supabase API URL and Key

**Setup Steps:**

1. **Get Your API Credentials:**
   ```
   Supabase Dashboard → Settings → API
   - Project URL: https://[your-project].supabase.co
   - API Key (anon/public): eyJhbGc...
   ```

2. **Create Power Query Connection:**
   ```excel
   Excel → Data → Get Data → From Other Sources → From Web
   ```

3. **Enter Supabase REST API URL:**
   ```
   https://[your-project].supabase.co/rest/v1/invoices?select=*
   ```

4. **Add Headers:**
   Click "Advanced" and add these headers:
   ```
   apikey: [your-anon-key]
   Authorization: Bearer [your-anon-key]
   ```

5. **Load Data:**
   - Excel will parse the JSON response
   - Transform columns as needed
   - Click "Close & Load"

6. **Set Auto-Refresh:**
   ```
   Right-click table → Refresh → Connection Properties
   → Enable "Refresh every X minutes"
   ```

**🎉 Result:** Your Excel sheet now auto-refreshes invoice data!

**Sample Power Query M Code:**
```m
let
    Source = Json.Document(Web.Contents(
        "https://[your-project].supabase.co/rest/v1/invoices",
        [
            Headers=[
                #"apikey"="[your-anon-key]",
                #"Authorization"="Bearer [your-anon-key]"
            ]
        ]
    )),
    ConvertedToTable = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    ExpandedRecords = Table.ExpandRecordColumn(ConvertedToTable, "Column1", 
        {"vendor_name", "invoice_number", "total_amount", "invoice_date"})
in
    ExpandedRecords
```

---

### Google Sheets - Apps Script (Auto-Sync)
**Best for:** Cloud-based automation, team dashboards

**Prerequisites:**
- Google account
- Supabase API credentials

**Setup Steps:**

1. **Open Google Sheets** and create new spreadsheet

2. **Open Apps Script:**
   ```
   Extensions → Apps Script
   ```

3. **Paste This Code:**
   ```javascript
   function fetchInvoices() {
     const SUPABASE_URL = 'https://[your-project].supabase.co';
     const SUPABASE_KEY = '[your-anon-key]';
     
     const url = `${SUPABASE_URL}/rest/v1/invoices?select=*`;
     
     const options = {
       'method': 'GET',
       'headers': {
         'apikey': SUPABASE_KEY,
         'Authorization': `Bearer ${SUPABASE_KEY}`
       }
     };
     
     const response = UrlFetchApp.fetch(url, options);
     const data = JSON.parse(response.getContentText());
     
     // Get active sheet
     const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
     
     // Clear existing data
     sheet.clear();
     
     // Add headers
     const headers = ['Vendor', 'Invoice #', 'Amount', 'Date', 'GST', 'Status'];
     sheet.appendRow(headers);
     
     // Add data rows
     data.forEach(invoice => {
       sheet.appendRow([
         invoice.vendor_name || 'N/A',
         invoice.invoice_number || 'N/A',
         invoice.total_amount || 0,
         invoice.invoice_date || 'N/A',
         (invoice.cgst + invoice.sgst + invoice.igst) || 0,
         invoice.payment_status || 'Unpaid'
       ]);
     });
     
     // Format as table
     const range = sheet.getDataRange();
     range.setFontFamily('Arial');
     sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
   }
   ```

4. **Replace Placeholders:**
   - Replace `[your-project]` with your Supabase project ID
   - Replace `[your-anon-key]` with your API key

5. **Save & Run:**
   - Save script (Ctrl+S)
   - Click "Run" button
   - Authorize the script (first time only)
   - Data appears in your sheet!

6. **Set Up Auto-Sync (Optional):**
   ```
   Apps Script → Triggers → Add Trigger
   → Function: fetchInvoices
   → Event: Time-driven
   → Type: Hour timer
   → Interval: Every hour
   ```

**🎉 Result:** Invoices auto-sync to Google Sheets every hour!

---

### Zoho Books Integration
**Best for:** Full accounting workflow, invoicing, inventory

**Method A: CSV Import (Simple)**
1. Export CSV from TrulyInvoice
2. Go to Zoho Books → Invoices
3. Click "Import" button
4. Upload CSV file
5. Map columns:
   - `vendor_name` → Customer Name
   - `invoice_number` → Invoice Number
   - `total_amount` → Total
   - `invoice_date` → Invoice Date

**Method B: API Integration (Advanced)**
Zoho Books has REST API - you can build custom sync:

```python
# Example: Sync TrulyInvoice → Zoho Books
import requests

# Get from Supabase
supabase_data = requests.get(
    'https://[your-project].supabase.co/rest/v1/invoices',
    headers={'apikey': 'your-key'}
).json()

# Push to Zoho
for invoice in supabase_data:
    zoho_response = requests.post(
        'https://books.zoho.com/api/v3/invoices',
        headers={'Authorization': 'Zoho-oauthtoken YOUR_TOKEN'},
        json={
            'customer_name': invoice['vendor_name'],
            'invoice_number': invoice['invoice_number'],
            'total': invoice['total_amount']
        }
    )
```

---

## 🤖 Method 3: No-Code Automation (Zapier/Make)

### Zapier Integration
**Best for:** Non-technical users, multi-app workflows

**Example: Auto-Add Invoices to Google Sheets**

1. **Create Zap:**
   - Trigger: Webhook (when invoice created)
   - Action: Add row to Google Sheets

2. **Set Up Webhook in Backend:**
   Add to your document processing endpoint:
   ```python
   # After creating invoice
   webhook_url = "https://hooks.zapier.com/hooks/catch/[your-id]"
   requests.post(webhook_url, json=invoice_data)
   ```

3. **Configure Google Sheets Action:**
   - Spreadsheet: Your invoice tracker
   - Worksheet: Sheet1
   - Map fields: vendor → Column A, amount → Column B, etc.

**Other Popular Zaps:**
- Invoice created → Send email to accountant
- High-value invoice → Notify on Slack
- New invoice → Create QuickBooks entry

---

### Make.com (Integromat)
Similar to Zapier but more visual:

1. Create new Scenario
2. Add Supabase module (HTTP request)
3. Add Google Sheets module
4. Map data fields
5. Set schedule (every hour, daily, etc.)

---

## 📊 Method 4: Enhanced Excel Export (Coming Soon)

We're building a better Excel export with:
- ✅ **Formatted headers** (bold, colored)
- ✅ **Borders** around cells
- ✅ **Currency formatting** (₹ symbol, 2 decimals)
- ✅ **Auto-width columns**
- ✅ **Multiple sheets** (Summary + Details)
- ✅ **Formulas** (SUM for totals)
- ✅ **Charts** (Monthly spending, vendor breakdown)

**Status:** In development 🚧

To implement, we'll add:
```python
# Backend: Use openpyxl instead of CSV
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, PatternFill

def export_to_excel(invoices):
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"
    
    # Headers with formatting
    headers = ['Vendor', 'Invoice #', 'Amount', 'Date', 'GST']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4472C4", fill_type="solid")
    
    # Data rows
    for inv in invoices:
        ws.append([
            inv['vendor_name'],
            inv['invoice_number'],
            inv['total_amount'],
            inv['invoice_date'],
            inv['cgst'] + inv['sgst'] + inv['igst']
        ])
    
    # Format currency column
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):
        for cell in row:
            cell.number_format = '₹#,##0.00'
    
    return wb
```

---

## 🔐 Security Best Practices

### API Key Management
**❌ DON'T:**
- Share your API keys publicly
- Commit keys to Git
- Use service_role key in frontend

**✅ DO:**
- Use anon/public key for client-side
- Store keys in environment variables
- Rotate keys periodically
- Enable RLS (Row Level Security)

### Row Level Security (RLS)
Your Supabase already has RLS enabled:
```sql
-- Users can only see their own invoices
CREATE POLICY "Users see own invoices"
ON invoices FOR SELECT
USING (auth.uid() = user_id);
```

This means:
- API integrations only fetch user's own data
- No risk of data leaks
- Safe to use anon key

---

## 🆘 Troubleshooting

### Excel Power Query: "Couldn't connect"
**Solution:**
- Check API URL is correct
- Verify API key in headers
- Try in browser first: `https://[project].supabase.co/rest/v1/invoices`

### Google Sheets: "Authorization required"
**Solution:**
- Apps Script → Run → Review permissions
- Allow script to access external URLs

### Zapier: "No data received"
**Solution:**
- Test webhook with Postman first
- Check webhook URL is active
- Verify JSON format

---

## 📚 Additional Resources

### API Documentation
- **Supabase REST API:** https://supabase.com/docs/guides/api
- **Google Sheets API:** https://developers.google.com/sheets/api
- **Zoho Books API:** https://www.zoho.com/books/api/v3/

### Video Tutorials
- Excel Power Query: [YouTube - "Connect Excel to REST API"](https://youtube.com)
- Google Apps Script: [YouTube - "Apps Script for Beginners"](https://youtube.com)

### Community Support
- Discord: [Your Discord Link]
- Email: support@trulyinvoice.com

---

## 🎯 Recommended Setup

**For Small Business (1-10 invoices/month):**
→ Use **CSV Export** to Excel/Google Sheets

**For Growing Business (10-50 invoices/month):**
→ Use **Google Sheets Apps Script** for auto-sync

**For Enterprise (50+ invoices/month):**
→ Use **Excel Power Query** + **Zapier** for full automation

---

## 🚀 What's Next?

We're building:
1. **Direct Excel Export** button (with formatting)
2. **QuickBooks Integration** (one-click sync)
3. **Webhooks** (real-time updates to external apps)
4. **Mobile API** (access invoices from any app)

---

**Need Help?** Open an issue on GitHub or email support@trulyinvoice.com

**Found a better integration method?** Submit a PR - we'd love to add it! 🎉
