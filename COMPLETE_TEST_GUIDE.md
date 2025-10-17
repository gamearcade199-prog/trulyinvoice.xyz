# 🎯 COMPLETE TEST GUIDE - EYE BUTTON & EXTRACTION

## ✅ What's Currently Running

```
BACKEND:  http://localhost:8000 ✅ (API keys loaded)
FRONTEND: http://localhost:3000 ✅ (Next.js running)
```

---

## 🧪 Test 1: Backend Health Check

### In Browser:
Go to: **http://localhost:8000/health**

Should see:
```json
{
  "status": "ok"
}
```

If you see this → Backend is working ✅

---

## 🧪 Test 2: Upload Invoice & Check Extraction

### Steps:

1. **Open Dashboard**
   - Go to: **http://localhost:3000/dashboard**
   - Should see "Upload Invoice" button

2. **Upload an Invoice**
   - Click "Upload Invoice"
   - Select an image (JPG/PNG) or PDF
   - Wait for processing

3. **Check Backend Logs**
   - Look at terminal running backend
   - Should see:
   ```
   📄 Processing: invoice.jpg for user ...
   📸 Image detected - using Vision API + Flash-Lite...
   ✅ BULLETPROOF GEMINI EXTRACTION
   ✅ AI extracted: [VENDOR NAME] - ₹[AMOUNT]
   ✅ Invoice created: [ID]
   ```

4. **Check Frontend**
   - Invoice should appear in list with:
     - Vendor name
     - Total amount
     - Date

---

## 👁️ Test 3: Click Eye Button (The Main Test)

### Steps:

1. **Find Invoice in List**
   - You should see uploaded invoice
   - Look for the 👁️ icon on the right

2. **Click Eye Button**
   - Click the 👁️ icon
   - Should navigate to invoice detail page

3. **Expected Result**
   ```
   ✅ Page loads (NO 404 error)
   ✅ Shows:
      - Invoice number
      - Vendor name
      - Total amount
      - Line items (if any)
      - Payment status
      - All extracted data
   ```

4. **Check Browser Console**
   - Press F12
   - Click Console tab
   - Should see:
   ```
   GET /api/invoices/[id] 200
   ```
   (NOT 404)

---

## 🔍 Test 4: Why It Works Now

### Before (Broken):
```
❌ Backend starts
❌ No API keys in environment
❌ Gemini extraction fails: "400 API Key not found"
❌ Invoice saved with ₹0.00
❌ Eye button shows 404 (no data to display)
```

### After (Fixed):
```
✅ Backend starts with API keys set
✅ Gemini extraction works
✅ Invoice saved with correct amount
✅ Eye button shows all details (no 404)
```

---

## 🛠️ Troubleshooting

### If Eye Button Still Shows 404:

1. **Check if new invoice was uploaded AFTER fix**
   - Old invoices with ₹0.00 won't work
   - Upload a NEW invoice

2. **Check backend logs for errors**
   - Copy any ERROR lines
   - Look for extraction failures

3. **Check frontend console (F12)**
   - Look for red error messages
   - Copy and share them

4. **Verify backend is running**
   - Check terminal for "Application startup complete"
   - Try health endpoint: http://localhost:8000/health

### If Backend Says "No API Keys":

Use the startup script:
```powershell
cd backend
.\START_BACKEND_WITH_API_KEYS.ps1
```

This ensures API keys are set BEFORE Python starts.

---

## 📋 Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Backend health check works
- [ ] Upload invoice
- [ ] Backend shows "✅ AI extracted"
- [ ] Invoice appears in list
- [ ] Click eye button
- [ ] Eye button shows invoice details (no 404)
- [ ] No errors in console (F12)

---

## ✅ Success Indicators

When everything works:

```
✅ Upload invoice → extraction succeeds
✅ Invoice saved with amount (NOT ₹0.00)
✅ Eye button → shows all details
✅ No 404 error
✅ Console shows 200 status
```

---

## 🎉 Next Steps

Once eye button works:
1. Test with different invoice types
2. Try bulk operations
3. Test export features
4. Everything else should work!

**Ready to test? Go to http://localhost:3000/dashboard**
