# 🎯 Export Template Quick Reference

## What Changed?
Users can now select how many sheets they want in their Excel exports when uploading invoices.

---

## 📋 User Experience

### Step 1: Upload Invoice
```
1. Go to Upload page (/upload)
2. See two template options:
   ✓ Simple (2 sheets)
   ✓ Accountant (5 sheets)
3. Select your preference
4. Upload invoice
```

### Step 2: Later, Export Invoice
```
1. Go to Invoices page (/invoices)
2. Find invoice → Click "Excel" export
3. Automatically exports with YOUR selected sheets
4. No need to select again!
```

---

## 📊 What Each Template Includes

### Simple (2 Sheets)
```
├── Sheet 1: Invoice Data
│   └── Basic invoice info, vendor, amounts
└── Sheet 2: Summary  
    └── Totals by payment status
```

### Accountant (5 Sheets)
```
├── Sheet 1: Invoice Data
├── Sheet 2: Summary
├── Sheet 3: GST Breakdown
├── Sheet 4: Line Items  
└── Sheet 5: Audit Trail
```

---

## 🔄 Where Is Your Preference Saved?

| Location | Format | Purpose |
|----------|--------|---------|
| **Database** | `users.export_template` | Main storage (survives logout) |
| **LocalStorage** | `export_template_{user_id}` | Backup in browser |
| **Backend** | Fetched on export | Used for generating sheets |

---

## ✨ Key Benefits

✅ **Remember Your Choice**: Preference saved in database
✅ **Consistent Exports**: Every export uses your preference  
✅ **No Manual Selection**: Template auto-applied on export
✅ **Works Everywhere**: Both invoice list and details pages
✅ **Privacy**: Only you see your preference

---

## 🧠 How Backend Uses Your Template

```python
# When you click export:
1. Backend gets your Bearer token
2. Validates authentication  
3. Queries: SELECT export_template FROM users WHERE id = your_id
4. Passes to: AccountantExcelExporter(template='accountant')
5. Exporter creates only sheets you requested
6. Sends Excel file to your browser
```

---

## 📸 Visual Flow

```
UPLOAD PAGE                   DATABASE              EXPORT ACTION
─────────────────            ────────────          ──────────────
Simple (2 sheets)  ──save──→ users table   ──read──→ Download Excel
Accountant (5)               export_     (on click)  with your sheets
                             template
                             ────────
```

---

## 🆚 Before vs After

### BEFORE
- Users got hardcoded 5 sheets every time
- No way to get fewer sheets
- Wasted download bandwidth for simple users

### AFTER  
- Users select at upload time
- Export respects their choice
- Smaller files for users who want simplicity
- Full details for users who need it

---

## ⚙️ Technical Implementation

```
Frontend Changes:
├── upload/page.tsx: Save template to DB after upload
├── invoices/details/page.tsx: Load template from DB on page load

Backend Changes:
└── api/invoices.py: Pass template parameter to exporter

Database:
└── users.export_template: Stores user's preference
```

---

## 🚀 Getting Started

No action needed! The feature is:
- ✅ Automatically implemented
- ✅ Database ready (column already exists)
- ✅ Working on both pages
- ✅ Backward compatible

Just start using it:

1. Go to upload page
2. Select your preferred template
3. Upload invoice
4. Export later → gets your template
5. Done! 🎉

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Export uses wrong sheets | Check if template was saved (check browser Dev Tools Console) |
| Template not saved | Ensure you're logged in before uploading |
| Fallback to default (5 sheets) | DB lookup failed, using accountant template |
| Wrong file size | Different templates = different sheet counts |

---

## 📞 Support

All three exporters now work with template system:
- ✅ Single invoice details export
- ✅ Bulk invoice list export  
- ✅ Both use same template preference

