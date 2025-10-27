═══════════════════════════════════════════════════════════════════════════════
                 🔧 REDIS CONNECTION STRING - COMPLETE GUIDE
═══════════════════════════════════════════════════════════════════════════════

YOU PROVIDED:
  redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

THIS IS INCOMPLETE - YOU NEED THE PASSWORD!

═══════════════════════════════════════════════════════════════════════════════
STEP 1: GET YOUR COMPLETE REDIS CONNECTION STRING
═══════════════════════════════════════════════════════════════════════════════

Go to Redis Cloud Dashboard: https://redis.com/
  1. Click "Databases"
  2. Click on your database (the one with port 11022)
  3. Look for "Connect" button or "Connection String" tab
  4. You'll see something like:

     redis://:YOUR_PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

  5. Copy the ENTIRE string (including the :password@)

FORMAT YOU NEED:
  redis://:YOUR_PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

EXAMPLE (NOT REAL):
  redis://:abc123xyz@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

═══════════════════════════════════════════════════════════════════════════════
STEP 2: ADD TO YOUR LOCAL .env FILE
═══════════════════════════════════════════════════════════════════════════════

File: c:\Users\akib\Desktop\trulyinvoice.xyz\.env

Replace this line:
  REDIS_URL=redis://localhost:6379/0

With this:
  REDIS_URL=redis://:YOUR_PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

COMPLETE EXAMPLE:
  REDIS_URL=redis://:mySecurePassword123@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

═══════════════════════════════════════════════════════════════════════════════
STEP 3: TEST LOCALLY
═══════════════════════════════════════════════════════════════════════════════

After updating .env, run:
  python test_redis_setup.py

You should see:
  ✅ REDIS SETUP COMPLETE!
  ✅ Connection successful
  ✅ Rate Limiting: Enabled
  ✅ Caching: Enabled

═══════════════════════════════════════════════════════════════════════════════
STEP 4: DEPLOY TO VERCEL or RENDER
═══════════════════════════════════════════════════════════════════════════════

YOUR QUESTION: Where should I add this in Render or Vercel?

ANSWER: Add to ENVIRONMENT VARIABLES

┌─────────────────────────────────────────────────────────────────────────────┐
│ FOR VERCEL:                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Go to: https://vercel.com/dashboard                                      │
│ 2. Click on your project                                                    │
│ 3. Click "Settings" tab                                                     │
│ 4. Click "Environment Variables" in left sidebar                            │
│ 5. Add new variable:                                                        │
│    Name:  REDIS_URL                                                         │
│    Value: redis://:YOUR_PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns...  │
│ 6. Click "Save"                                                             │
│ 7. Re-deploy (new deployment with updated env vars)                         │
│                                                                             │
│ ALL ENVIRONMENTS (Recommended):                                             │
│ ☐ Production                                                               │
│ ☐ Preview                                                                  │
│ ☐ Development                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FOR RENDER:                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Go to: https://render.com/dashboard                                      │
│ 2. Click on your service                                                    │
│ 3. Click "Environment" tab at top                                           │
│ 4. Scroll to "Environment Variables"                                        │
│ 5. Add new variable:                                                        │
│    Key:   REDIS_URL                                                         │
│    Value: redis://:YOUR_PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns...  │
│ 6. Click "Save"                                                             │
│ 7. Service will auto-redeploy with new env vars                             │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
STEP 5: WHAT ABOUT OTHER ENVIRONMENT VARIABLES?
═══════════════════════════════════════════════════════════════════════════════

You should also add these to Vercel/Render for production:

CRITICAL (Must have):
  • REDIS_URL          ← The one we're doing now
  • DATABASE_URL       ← Your PostgreSQL/Supabase database
  • RAZORPAY_KEY_ID    ← Your Razorpay production key (NOT test key!)
  • RAZORPAY_KEY_SECRET
  • SECRET_KEY         ← Change to random production value

IMPORTANT (Recommended):
  • SENTRY_DSN         ← For error tracking
  • GEMINI_API_KEY     ← For AI features
  • SUPABASE_URL       ← For file storage
  • SUPABASE_KEY

OPTIONAL (Nice to have):
  • ENVIRONMENT        ← Set to "production"
  • DEBUG              ← Set to "false"

═══════════════════════════════════════════════════════════════════════════════
DO NOT DO THIS:
═══════════════════════════════════════════════════════════════════════════════

❌ DON'T commit .env file to git
   - It has your secrets!
   - Already in .gitignore (check)

❌ DON'T use the same test/development values in production
   - RAZORPAY: Must use rzp_live_* (not rzp_test_*)
   - ENVIRONMENT: Must be "production" (not "development")

❌ DON'T copy connection string to multiple places and forget to update them all
   - One source of truth: Your deployment platform's env vars

❌ DON'T forget to re-deploy after adding env vars
   - Vercel: Auto-redeploys (sometimes)
   - Render: Usually auto-redeploys
   - Always verify it deployed

═══════════════════════════════════════════════════════════════════════════════
STEP-BY-STEP FOR YOUR SETUP:
═══════════════════════════════════════════════════════════════════════════════

1. LOCAL DEVELOPMENT (Now):
   └─ Update .env file with full Redis URL
   └─ Run: python test_redis_setup.py
   └─ Verify: ✅ Shows all green

2. DEPLOYMENT (When ready):
   └─ Go to Vercel/Render dashboard
   └─ Add REDIS_URL to environment variables
   └─ Make sure to include password!
   └─ Re-deploy

3. VERIFY PRODUCTION:
   └─ Check your deployment logs
   └─ Should see: "✅ Redis cache layer initialized"
   └─ Test API endpoint
   └─ Check Redis Cloud dashboard for live connections

═══════════════════════════════════════════════════════════════════════════════
REDIS CONNECTION STRING PARTS EXPLAINED:
═══════════════════════════════════════════════════════════════════════════════

Format: redis://:password@host:port/db

Your Redis:
  redis://:YOUR_PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

  redis://        ← Protocol
  :               ← Separator
  YOUR_PASSWORD   ← Your Redis password (from Redis Cloud dashboard)
  @               ← Separator
  redis-11022...  ← Your Redis host
  :11022          ← Your Redis port (11022 in your case, not the default 6379)
  (no /db)        ← Default database (0)

═══════════════════════════════════════════════════════════════════════════════
QUICK REFERENCE:
═══════════════════════════════════════════════════════════════════════════════

Local Development:
  .env file: REDIS_URL=redis://:password@redis-11022...

Production (Vercel):
  Settings → Environment Variables → Add REDIS_URL

Production (Render):
  Environment tab → Environment Variables → Add REDIS_URL

═══════════════════════════════════════════════════════════════════════════════

NEXT: Get your complete connection string with password and tell me!
I'll help you set it up on Vercel/Render.

═══════════════════════════════════════════════════════════════════════════════
