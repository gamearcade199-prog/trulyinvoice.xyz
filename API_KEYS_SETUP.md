# 🔑 API Keys Setup Guide

## You need to add YOUR API keys to get the backend running!

### Open the file: `backend\.env`

Replace these placeholders with your actual keys:

---

## 1. ✅ OpenAI API Key (YOU HAVE THIS!)

```env
OPENAI_API_KEY=sk-proj-your-actual-openai-key-here
```

**Where to find it:**
- Go to: https://platform.openai.com/api-keys
- Copy your existing key or create a new one
- Paste it in the `.env` file

---

## 2. 🔑 Google Cloud Vision Credentials

**Option A: Using Service Account JSON (Recommended)**

1. Go to: https://console.cloud.google.com/
2. Create/select a project
3. Enable "Cloud Vision API"
4. Create Service Account:
   - IAM & Admin → Service Accounts → Create
   - Grant role: "Cloud Vision API User"
   - Create JSON key and download it
5. Save the JSON file somewhere safe (e.g., `C:\trulyinvoice-keys\google-vision.json`)
6. Update `.env`:

```env
GOOGLE_CLOUD_VISION_CREDENTIALS=C:\trulyinvoice-keys\google-vision.json
```

**OR Option B: Using Environment Variable (PowerShell)**

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account.json"
```

---

## 3. 🗄️ Supabase Database (Required)

1. Go to: https://supabase.com/
2. Create new project (takes 2-3 minutes to set up)
3. Go to Project Settings → Database
4. Copy the "Connection string" (URI format)
5. Update `.env`:

```env
DATABASE_URL=postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

Also get your Supabase API keys:
- Go to Project Settings → API
- Copy these values:

```env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here
```

---

## 4. 🔐 Secret Key (Generate Random String)

```env
SECRET_KEY=ThisIsAVerySecureRandomString12345ChangeThisToSomethingRandom
```

You can use any random string (at least 32 characters).

---

## ✅ Once you've added all keys:

### Test the backend:

```powershell
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

You should see the API documentation!

---

## 📝 Summary of What You Need:

- [x] OpenAI API Key (you have this!)
- [ ] Google Cloud Vision Service Account JSON
- [ ] Supabase Project (database + keys)
- [ ] Random secret key for JWT

Let me know once you have these ready and I'll help you test the setup!
