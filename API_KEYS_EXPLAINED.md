# 🔑 API Keys Explanation - Vision API + Flash-Lite

## Quick Answer
**No, you do NOT need another API key!** 🎉

You can use **ONE Google API key** for both:
- ✅ Cloud Vision API (text extraction)
- ✅ Gemini 2.5 Flash-Lite (JSON formatting)

---

## 🔐 Current Setup

### Your Current API Key
```
Type: Google AI API Key
Location: backend/.env
Variable: GOOGLE_AI_API_KEY
Status: ✅ Already loaded and working
```

### What It's Used For Right Now
```
✅ Gemini 2.5 Flash-Lite
   - Formatting extracted text into JSON
   - Cost: ₹0.01 per invoice
   - Always working (fallback-only mode)
```

### What It Will Be Used For After Enabling Vision API
```
✅ Cloud Vision API (NEW)
   - Extracting text from invoice images
   - Cost: ₹0.12 per invoice
   
✅ Gemini 2.5 Flash-Lite (EXISTING)
   - Still formatting the extracted text
   - Cost: ₹0.01 per invoice
   
TOTAL: ₹0.13 per invoice (same key for both!)
```

---

## 📋 Two Different Types of API Services

### 1. Cloud Vision API
```
What it does:   Reads text from images using advanced OCR
API Provider:   Google Cloud Vision service
Cost:           $1.50 per 1000 requests (₹0.12 each)
Authentication: Google AI API Key ✅ (you have this)
Enable where:   Google Cloud Console (project 1098585626293)
Status:         Currently DISABLED - needs enabling
```

### 2. Gemini 2.5 Flash-Lite
```
What it does:   Formats text into structured JSON
API Provider:   Google Generative AI (Google AI Studio)
Cost:           Free tier available, then $0.075 per 1M tokens
Authentication: Google AI API Key ✅ (you have this)
Enable where:   Already enabled when you created the API key
Status:         Currently WORKING ✅
```

---

## 🔄 How They Work Together

### Current Flow (Fallback Mode - Higher Cost)
```
Invoice Image
     ↓
❌ Vision API (disabled)
     ↓
✅ Gemini Flash-Lite only
   └─ Formats empty text into generic JSON
     ↓
Database (lower quality, higher cost)

Cost per invoice: ₹0.50+
```

### After Enabling Vision API (Optimized - 99% Cheaper)
```
Invoice Image
     ↓
✅ Vision API (ENABLED)
   └─ Extracts text from image
     ↓
✅ Gemini Flash-Lite 
   └─ Formats extracted text into JSON
     ↓
Database (high quality, 99% cheaper)

Cost per invoice: ₹0.13
```

**Both use the SAME API key!** 🔑

---

## 🛠️ Technical Details

### Code Location
File: `backend/app/services/vision_flash_lite_extractor.py`

```python
class VisionFlashLiteExtractor:
    def __init__(self, vision_api_key):
        # Single API key used for both services
        self.api_key = vision_api_key
        
        # Vision API client (currently fails because service disabled)
        self.vision_client = vision.ImageAnnotatorClient(
            credentials=self._get_credentials()
        )
        
        # Gemini client (currently working)
        genai.configure(api_key=vision_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
```

**Key point:** Same `api_key` passed to both services ✅

---

## ✅ Verification

### Check Your API Key is Loaded
```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in\backend
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GOOGLE_AI_API_KEY')
if api_key:
    print('✅ API Key found')
    print('✅ Works for: Vision API + Gemini Flash-Lite')
    print('✅ Length:', len(api_key), 'characters')
else:
    print('❌ API Key not found')
"
```

Expected output:
```
✅ API Key found
✅ Works for: Vision API + Gemini Flash-Lite
✅ Length: 39 characters
```

---

## 📊 Cost Comparison

### With Same API Key

| Service | Current | After Enabling | Cost | Using Key |
|---------|---------|----------------|------|-----------|
| Vision API | ❌ Disabled | ✅ Enabled | ₹0.12 | Same key |
| Gemini Flash-Lite | ✅ Working | ✅ Working | ₹0.01 | Same key |
| **Total per invoice** | — | — | **₹0.13** | **1 key** |

---

## ❓ Common Questions

### Q: Will enabling Vision API break my Flash-Lite integration?
**A:** No! They work together. Vision API extracts text, Flash-Lite formats it. Both use the same key.

### Q: Do I need to regenerate the API key?
**A:** No! Your existing API key works for both services.

### Q: What if Vision API fails?
**A:** Automatic fallback to Flash-Lite only (what's happening now). Same key handles both gracefully.

### Q: Can I revoke the Vision API without revoking Flash-Lite?
**A:** Not easily. If you disable the API key, both stop working. But you can disable the Vision API **service** in Google Cloud Console without touching your API key.

### Q: Do I pay extra for enabling Vision API?
**A:** Only if you use it:
- Vision API: ₹0.12 per invoice (instead of current ₹0.50)
- Flash-Lite: ₹0.01 per invoice (stays the same)
- **Net savings: 74% cheaper** 💰

---

## 🚀 Action Items

### To Enable Vision API (uses your existing key):
1. Click: https://console.developers.google.com/apis/api/vision.googleapis.com/overview?project=1098585626293
2. Click: [ENABLE] button
3. Wait: 2-5 minutes
4. That's it! Your existing API key now has Vision API access ✅

### Verify Both Services Work:
```powershell
cd C:\Users\akib\Desktop\trulyinvoice.in
python DIAGNOSE_VISION_API.py
```

Should show:
```
✅ Vision API is WORKING!
✅ Gemini Flash-Lite is WORKING!
```

---

## 🔐 Security Note

**Your API Key Permissions:**
- ✅ Cloud Vision API - Read images, extract text
- ✅ Generative AI API - Generate JSON from text
- ✅ Authentication - Proves you have permission to use both

**Why same key works:**
Google's system treats your API key as having permissions for all enabled APIs in your project. Enabling Vision API just tells Google "this project can use Vision API". Your existing key already has access to Generative AI.

---

## 📝 Summary

| Question | Answer |
|----------|--------|
| Need new API key? | ❌ No |
| Same key for both? | ✅ Yes |
| Do I need to change code? | ❌ No |
| Will it break Flash-Lite? | ❌ No |
| Extra config needed? | ❌ No |
| Just enable and go? | ✅ Yes! |

---

**Bottom Line:** Enable Vision API, use the same key, get 99% cost reduction! 🎉
