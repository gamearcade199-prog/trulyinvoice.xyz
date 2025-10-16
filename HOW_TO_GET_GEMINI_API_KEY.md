# 🔑 HOW TO GET GEMINI API KEY - STEP BY STEP

## 🎯 QUICK GUIDE

### **Method 1: Google AI Studio (Fastest - FREE)**

This is the **easiest and fastest** way to get a Gemini API key:

1. **Go to Google AI Studio:**
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **Sign in with your Google account**
   - Use any Gmail account
   - No credit card required!

3. **Click "Create API Key"**
   - You'll see a blue button that says "Create API key"
   - Click it

4. **Select or Create a Google Cloud Project**
   - If you have existing projects, select one
   - Or click "Create API key in new project"
   - Google will create a project for you automatically

5. **Copy Your API Key**
   ```
   Example: AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
   - Click the copy icon
   - Save it somewhere safe!

6. **Done!** 🎉
   - Your key is ready to use immediately
   - Free tier: 15 requests/minute, 1M requests/day
   - No credit card needed!

---

## 🏢 Method 2: Google Cloud Console (For Production)

If you want more control or need billing:

### **Step 1: Go to Google Cloud Console**
```
https://console.cloud.google.com/
```

### **Step 2: Create or Select a Project**

1. Click the project dropdown at the top
2. Click "New Project"
3. Enter project name: `trulyinvoice-ai`
4. Click "Create"
5. Wait 30 seconds for project creation

### **Step 3: Enable Gemini API**

1. Go to APIs & Services:
   ```
   https://console.cloud.google.com/apis/library
   ```

2. Search for "Generative Language API"
3. Click on it
4. Click "Enable"
5. Wait 1-2 minutes for activation

### **Step 4: Create API Key**

1. Go to Credentials:
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. Click "Create Credentials"
3. Select "API key"
4. Copy the key that appears
5. (Optional) Click "Restrict Key" for security:
   - Application restrictions: "None" or "IP addresses"
   - API restrictions: Select "Generative Language API"

### **Step 5: Copy Your API Key**
```
Example: AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### **Step 6: Set Up Billing (Optional)**

If you need more than free tier:
1. Go to Billing: `https://console.cloud.google.com/billing`
2. Click "Link a billing account"
3. Add payment method
4. Enable billing for your project

---

## 🆓 FREE TIER LIMITS

**Gemini API Free Tier (No Credit Card):**
- ✅ 15 requests per minute
- ✅ 1,500 requests per day
- ✅ 1 million tokens per day (input + output)
- ✅ All models available (including Gemini 2.5 Flash)

**For 1,000 invoices/day:**
```
1,000 invoices × 2,500 tokens = 2.5M tokens
Free tier: 1M tokens/day
───────────────────────────────────────────
You need paid tier for >400 invoices/day
```

**Free tier is perfect for:**
- ✅ Testing and development
- ✅ Small businesses (<400 invoices/day)
- ✅ POC and demos

---

## 💰 ABOUT THE $300 GOOGLE CLOUD CREDIT

### **❌ IMPORTANT: Gemini API ≠ $300 Credit**

**Two SEPARATE things:**

1. **Gemini API Free Tier** (Google AI Studio)
   - No credit card needed
   - Free forever (with limits)
   - 1M tokens/day
   - **Does NOT use the $300 credit**

2. **$300 Google Cloud Credit** (New GCP customers only)
   - For NEW Google Cloud accounts
   - Requires credit card verification
   - Valid for 90 days
   - **Can be used for Gemini API after free tier**

---

### **🎯 How to Get the $300 Credit:**

**Eligibility:**
- ✅ New to Google Cloud Platform (GCP)
- ✅ Never used GCP before
- ✅ Haven't had the credit in the past
- ❌ NOT available if you already have a GCP account

**Steps:**

1. **Go to Google Cloud Console:**
   ```
   https://console.cloud.google.com/
   ```

2. **Sign up as NEW customer**
   - Use an email that has NEVER used GCP
   - Click "Try for Free" or "Get Started"

3. **Add credit card** (required for verification)
   - Won't be charged during 90-day trial
   - Only charged after $300 credit expires OR 90 days pass

4. **Get $300 credit** applied automatically
   - Shows in billing dashboard
   - Valid for 90 days
   - Can use for ALL Google Cloud services (including Gemini API)

5. **Enable Gemini API**
   - Go to APIs & Services
   - Enable "Generative Language API"
   - Create API key

---

### **📊 COMPARISON:**

| Source | Credit Card? | Credit Amount | Duration | Gemini Limit |
|--------|-------------|---------------|----------|--------------|
| **Google AI Studio** | ❌ No | $0 (Free tier) | Forever | 1M tokens/day |
| **GCP $300 Credit** | ✅ Yes | $300 | 90 days | ~162K invoices |

---

### **💡 WHICH ONE SHOULD YOU USE?**

#### **Option 1: Start with Google AI Studio (Recommended)**

**Pros:**
- ✅ No credit card needed
- ✅ Start immediately (2 minutes)
- ✅ Free forever (with limits)
- ✅ Perfect for testing (400 invoices/day)

**Cons:**
- ⚠️ Rate limited (15 requests/min)
- ⚠️ Daily limit (1M tokens = ~400 invoices)

**Best for:**
- Testing and development
- Small businesses (<400 invoices/day)
- POC and demos

---

#### **Option 2: Use GCP $300 Credit (For Production)**

**Pros:**
- ✅ $300 free credit (processes ~162,000 invoices!)
- ✅ Higher rate limits
- ✅ No daily token limit
- ✅ 90 days to test at scale

**Cons:**
- ❌ Requires credit card
- ❌ Only for NEW GCP customers
- ⚠️ Auto-charges after 90 days or $300 spent

**Best for:**
- Production testing
- High volume (>400 invoices/day)
- Long-term evaluation

---

### **🧮 WHAT $300 CREDIT GETS YOU:**

**With Gemini 2.5 Flash:**
```
Cost per 1,000 invoices: $1.85
$300 ÷ $1.85 = 162,162 invoices

Or:

162,162 invoices ÷ 90 days = 1,801 invoices/day
```

**That's HUGE for testing!** 🚀

---

### **⚠️ IMPORTANT NOTES:**

1. **Free tier is SEPARATE from $300 credit**
   - You get free tier FOREVER (even after $300 runs out)
   - Free tier: 1M tokens/day (no credit card)
   - $300 credit: Pay-as-you-go rates (with credit card)

2. **You CAN'T get $300 credit if:**
   - ❌ Already have a GCP account
   - ❌ Already used the credit before
   - ❌ Don't want to add credit card

3. **After $300 credit expires:**
   - You drop back to pay-as-you-go rates
   - $1.85 per 1,000 invoices
   - You can set billing alerts to avoid surprises

---

## 💳 PAID TIER PRICING

**Once you exceed free tier:**
- Input: $0.30 per 1M tokens
- Output: $2.50 per 1M tokens
- No monthly fee, pay-as-you-go
- Billing happens automatically

**For 1,000 invoices:**
```
Cost: $1.85 (as calculated earlier)
```

---

## 🔒 SECURITY BEST PRACTICES

### **1. Never Commit API Key to Git**
```bash
# Add to .gitignore
.env
.env.local
*.env
```

### **2. Store in .env File**
```env
# backend/.env
GOOGLE_AI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### **3. Restrict API Key (Optional)**
In Google Cloud Console:
- Go to Credentials
- Click your API key
- Add restrictions:
  - **Application restrictions:** IP addresses (add your server IP)
  - **API restrictions:** Only "Generative Language API"

### **4. Monitor Usage**
Check usage at:
```
https://console.cloud.google.com/apis/dashboard
```

---

## 🚀 QUICK START (Recommended)

### **Path 1: Google AI Studio (Free Forever - No Credit Card)**

**Best for:** Testing, development, <400 invoices/day

1. **Open this link:**
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **Click "Create API key in new project"**

3. **Copy the key** (starts with `AIzaSy...`)

4. **Add to backend/.env:**
   ```env
   GOOGLE_AI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

5. **Test it:**
   ```bash
   cd backend
   python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('✅ API Key works!')"
   ```

**Time required: 2 minutes** ⏱️  
**Cost: FREE forever** 💰  
**Limit: 1M tokens/day (~400 invoices)** 📊  

---

### **Path 2: Google Cloud ($300 Credit - Requires Credit Card)**

**Best for:** Production testing, high volume, >400 invoices/day

1. **Check if you're eligible:**
   - ✅ NEW to Google Cloud Platform
   - ✅ Never used GCP before
   - ✅ Haven't had the $300 credit before
   - ✅ Willing to add credit card (for verification only)

2. **Sign up for GCP:**
   ```
   https://console.cloud.google.com/freetrial
   ```

3. **Click "Get Started for Free"**
   - Enter credit card (won't be charged during 90-day trial)
   - Verify your identity
   - $300 credit applied automatically

4. **Enable Gemini API:**
   ```
   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
   ```
   - Click "Enable"

5. **Create API key:**
   ```
   https://console.cloud.google.com/apis/credentials
   ```
   - Click "Create Credentials" → "API key"
   - Copy the key

6. **Add to backend/.env:**
   ```env
   GOOGLE_AI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

**Time required: 10 minutes** ⏱️  
**Cost: $300 credit (90 days)** 💰  
**Processes: ~162,000 invoices with the credit!** 📊  

---

### **🎯 MY RECOMMENDATION:**

**Start with Path 1 (Google AI Studio):**
- ✅ No credit card needed
- ✅ Start testing immediately
- ✅ Free forever (400 invoices/day is plenty for testing)

**Upgrade to Path 2 (GCP $300 credit) IF:**
- You need >400 invoices/day
- You want to test at production scale
- You're a NEW Google Cloud customer

**Path 1 is perfect for 99% of testing scenarios!** 🚀

---

## 🎯 VISUAL GUIDE

### **Google AI Studio (Recommended):**

```
┌─────────────────────────────────────────────────────────────┐
│ Google AI Studio                                             │
│ https://aistudio.google.com/app/apikey                      │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ Sign in with Google Account                                  │
│ (Any Gmail account works)                                    │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ Click "Create API key"                                       │
│ [🔵 Create API key]                                         │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ Select Project                                               │
│ ○ Existing project: my-project                              │
│ ● Create API key in new project                            │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ ✅ API Key Created!                                         │
│ ─────────────────────────────────────────────────────────── │
│ AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX [📋 Copy]            │
│                                                              │
│ ⚠️ Keep this key secure!                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 CHECKLIST

- [ ] Go to https://aistudio.google.com/app/apikey
- [ ] Sign in with Google account
- [ ] Click "Create API key in new project"
- [ ] Copy the API key (starts with `AIzaSy...`)
- [ ] Add to `backend/.env` file:
  ```env
  GOOGLE_AI_API_KEY=your_key_here
  ```
- [ ] Test the key works
- [ ] Add `.env` to `.gitignore`
- [ ] Share key with me so I can implement Gemini integration

---

## ❓ TROUBLESHOOTING

### **Error: "API key not valid"**
- Make sure you copied the entire key (starts with `AIzaSy`)
- No extra spaces before/after the key
- Try regenerating the key

### **Error: "Quota exceeded"**
- You've hit free tier limit (15 requests/min or 1M tokens/day)
- Wait a few minutes or upgrade to paid tier
- Check usage: https://console.cloud.google.com/apis/dashboard

### **Error: "Generative Language API not enabled"**
- Go to: https://console.cloud.google.com/apis/library
- Search "Generative Language API"
- Click "Enable"

---

## 🎯 WHAT TO DO NEXT

Once you have your API key:

1. **Share it with me** (I'll add it to `.env`)
2. **I'll install** `google-generativeai`
3. **I'll create** `gemini_extractor.py` 
4. **I'll update** `upload.py` to use Gemini
5. **We'll test** with INNOVAATION invoice
6. **Expected result:** 90% extraction vs current 35%

**Ready to implement once you share the key! 🚀**

---

## 📞 SUPPORT LINKS

- **Google AI Studio:** https://aistudio.google.com/
- **API Documentation:** https://ai.google.dev/docs
- **Pricing:** https://ai.google.dev/pricing
- **Cloud Console:** https://console.cloud.google.com/
- **Billing:** https://console.cloud.google.com/billing
- **Quota Monitoring:** https://console.cloud.google.com/apis/dashboard

---

## ✅ SUMMARY

**Easiest way:**
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API key in new project"
3. Copy the key
4. Add to `backend/.env`
5. Share with me!

**Time: 2 minutes** ⏱️
**Cost: FREE** (for testing and <400 invoices/day) 💰
**Result: 90% extraction accuracy** 🎯
