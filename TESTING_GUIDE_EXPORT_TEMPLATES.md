# 🧪 Testing Guide: Export Template Feature

## ✅ Quick Test

### Test 1: Simple Template Export

```
Step 1: Go to http://localhost:3000/upload
Step 2: Select "Simple (2 sheets)" radio button
Step 3: Upload any invoice
Step 4: Check backend log → should save template="simple"
Step 5: Go to http://localhost:3000/invoices
Step 6: Click on invoice → "View Details"
Step 7: Click "Export Excel"
Step 8: Check backend log → should show "Template: simple"
Step 9: Download Excel and verify → 2 sheets
```

**Expected Result**: ✅ Excel has 2 sheets (Invoice Data + Summary)

---

### Test 2: Accountant Template Export

```
Step 1: Clear browser localStorage (Optional) or use different user
Step 2: Go to http://localhost:3000/upload
Step 3: Select "Accountant (5 sheets)" radio button
Step 4: Upload an invoice
Step 5: Check backend log → should save template="accountant"
Step 6: Go to http://localhost:3000/invoices
Step 7: Click on invoice → "View Details"
Step 8: Click "Export Excel"
Step 9: Check backend log → should show "Template: accountant"
Step 10: Download Excel and verify → 5 sheets
```

**Expected Result**: ✅ Excel has 5 sheets (Data, Summary, GST, Line Items, Audit)

---

### Test 3: Template Persistence

```
Step 1: Upload invoice with "Simple (2 sheets)"
Step 2: Close browser completely
Step 3: Log out from Supabase
Step 4: Log back in
Step 5: Go to any invoice and click export
Step 6: Check backend log → should STILL show "Template: simple"
Step 7: Download Excel → should STILL have 2 sheets
```

**Expected Result**: ✅ Template preference persists across sessions

---

## 🔍 Debugging: Check Backend Logs

### What to Look For

**Good Logs**:
```
✅ Export-Excel: Processing invoice...
✅ User authenticated: [user-id]
   📋 Using template: accountant        ← IMPORTANT LINE
   ✅ Professional Excel export completed
   📊 1 invoices, 1 line items
   🎨 Template: accountant              ← CONFIRMATION
```

**Bad Logs** (Missing Template):
```
❌ Could not fetch template preference, using default 'accountant'
```

---

## 📊 Backend Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 OK | Export successful | ✅ File downloads |
| 401 Unauthorized | No/invalid token | ❌ Check Bearer token in request |
| 404 Not Found | Invoice doesn't exist | ❌ Check invoice ID |
| 500 Server Error | Export failed | ❌ Check backend logs |

---

## 🔐 Browser DevTools Check

### Console Tab:
```javascript
// Should see:
"📋 Loaded export template from DB: accountant"
"✅ [format] exported successfully"
```

### Network Tab:
```
GET /api/invoices/{id}/export-excel
Status: 200 OK
Headers:
  ✓ Authorization: Bearer eyJhbGc...
  ✓ Content-Type: application/vnd.openxmlformats-office...
```

---

## 🗂️ File System Check

After export, check your Downloads folder:

**Simple (2 sheets)**:
```
bulk_invoices_simple_20251023_124435.xlsx
├── Sheet: "Invoice Data"
└── Sheet: "Summary"
```

**Accountant (5 sheets)**:
```
bulk_invoices_accountant_20251023_124435.xlsx
├── Sheet: "Invoice Data"
├── Sheet: "Summary"
├── Sheet: "GST Breakdown"
├── Sheet: "Line Items"
└── Sheet: "Audit Trail"
```

---

## 🐛 Troubleshooting

### Issue: Export returns 401 Unauthorized

**Cause**: Authorization header missing or invalid

**Fix**:
1. Make sure you're logged in
2. Check token expiration
3. Try logging out and back in
4. Check DevTools Console for token errors

### Issue: Template shows as "accountant" but user selected "simple"

**Cause**: Database preference not saved

**Fix**:
1. Check browser console for save errors
2. Verify users table has `export_template` column:
   ```sql
   SELECT column_name FROM information_schema.columns 
   WHERE table_name = 'users';
   ```
3. Check user's record:
   ```sql
   SELECT id, export_template FROM users LIMIT 1;
   ```

### Issue: Excel always has 5 sheets

**Cause**: Template preference not being read

**Fix**:
1. Check backend logs for "Using template:" message
2. Verify Supabase query working:
   ```python
   users_response = supabase.table("users").select("export_template").eq("id", user_id).execute()
   print(users_response.data)
   ```

---

## ✅ Manual Verification

### Step 1: Check Database

```bash
# In Supabase SQL Editor
SELECT id, email, export_template FROM users WHERE export_template IS NOT NULL;
```

Should return something like:
```
id                                   | email              | export_template
d1949c37-d380-46f4-ad30-20ae84aff1ad | user@example.com   | simple
```

### Step 2: Check Frontend State

Open DevTools Console and run:
```javascript
localStorage.getItem('export_template_d1949c37-d380-46f4-ad30-20ae84aff1ad')
// Should return: "simple" or "accountant"
```

### Step 3: Check Backend Logic

Look for these logs in backend terminal:
```
📋 Using template: simple          ← Template being read
✅ Professional Excel export completed
🎨 Template: simple                ← Template being used
```

---

## 📈 Success Metrics

- ✅ Template selected during upload is saved
- ✅ Template loaded when viewing invoice details  
- ✅ Correct number of sheets in Excel export
- ✅ Template persists across sessions
- ✅ Backend logs show template is being used
- ✅ Export file download completes
- ✅ No errors in browser console
- ✅ No errors in backend logs

---

## 🎯 Expected Test Results

| Action | Expected Result |
|--------|-----------------|
| Select "Simple" + Upload | ✅ `export_template = "simple"` saved |
| Select "Accountant" + Upload | ✅ `export_template = "accountant"` saved |
| Export from details page | ✅ Uses saved template |
| Export from list page | ✅ Uses saved template |
| Log out/in + Export | ✅ Still uses saved template |
| Browser DevTools Console | ✅ No errors about template |
| Backend Logs | ✅ Shows "Using template: [preference]" |
| Downloaded Excel | ✅ Has correct sheet count |

---

## 🚀 Full End-to-End Test

```
UPLOAD → SAVE → VERIFY → EXPORT → DOWNLOAD → VERIFY

1. Upload page with preference selection
   └─→ Frontend saves to DB: users.export_template
   
2. Backend confirmation
   └─→ Logs: "Saved template preference to database: [choice]"
   
3. Invoice details page loads
   └─→ Frontend fetches from DB: SELECT export_template FROM users
   └─→ Sets state: exportTemplate = [preference]
   
4. Click Export button
   └─→ Backend receives request
   └─→ Fetches from DB: SELECT export_template FROM users
   └─→ Logs: "Using template: [preference]"
   
5. Exporter uses template
   └─→ Logs: "Template: [preference]"
   └─→ Creates Excel with appropriate sheets
   
6. Browser downloads file
   └─→ File contains correct sheets
   └─→ Logs: "✅ [format] exported successfully"
   
7. Verify in Excel
   └─→ Count sheets
   └─→ Match to template choice
```

---

## 📞 If Something Goes Wrong

1. **Check console logs** (browser DevTools)
2. **Check backend logs** (terminal where uvicorn is running)
3. **Check database** (Supabase SQL Editor)
4. **Restart backend**: Press Ctrl+C and rerun `uvicorn`
5. **Clear browser cache**: Ctrl+Shift+Delete
6. **Re-login**: Log out and back in

---

## ✨ Success! 

When everything works:
- ✅ User selects template at upload
- ✅ Backend logs confirm template saved
- ✅ User exports invoice
- ✅ Backend logs confirm template used  
- ✅ Excel file has correct number of sheets
- ✅ Feature works on next login too

**You're done!** 🎉

