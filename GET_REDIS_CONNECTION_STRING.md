╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              📍 HOW TO GET YOUR REDIS CONNECTION STRING 📍                 ║
║                                                                            ║
║                   Step-by-Step Visual Guide                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
YOUR REDIS DATABASE:
═══════════════════════════════════════════════════════════════════════════════

Database Name: database-MH910T3P
Status: ✅ Active (green dot)
Memory: 2.5MB / 30MB
Endpoint: redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

═══════════════════════════════════════════════════════════════════════════════
STEP 1: Click "Connect" Button
═══════════════════════════════════════════════════════════════════════════════

You're in the Redis Cloud Console.
You can see your database "database-MH910T3P" in the list.

To get your connection string:
1. Look for the "Connect" button (usually blue or in the row)
2. It should be in your database row on the right side
3. Click it

═══════════════════════════════════════════════════════════════════════════════
STEP 2: Select Connection Method
═══════════════════════════════════════════════════════════════════════════════

After clicking Connect, you'll see options like:
- Redis Client
- Redis CLI
- Docker
- Node.js
- Python
- etc.

SELECT: "Redis CLI" or the option that shows the connection URL

═══════════════════════════════════════════════════════════════════════════════
STEP 3: Copy the Connection String
═══════════════════════════════════════════════════════════════════════════════

You'll see a connection string in one of these formats:

FORMAT 1 (Most Common):
  redis://:PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

FORMAT 2 (Alternative):
  redis://:PASSWORD@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022/0

IMPORTANT: Your format will be something like:
  redis://:yourPasswordHere@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

KEY PARTS:
  redis://           ← Protocol (always this)
  :                  ← Separator
  PASSWORD           ← Your actual Redis password (this is what you need!)
  @                  ← Separator
  redis-11022...     ← Your host
  :11022             ← Your port

═══════════════════════════════════════════════════════════════════════════════
WHAT THE CONNECTION STRING LOOKS LIKE:
═══════════════════════════════════════════════════════════════════════════════

BEFORE (What you see on screen):
  redis://:abc123XYZ789@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

AFTER (What we'll use):
  REDIS_URL=redis://:abc123XYZ789@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022

═══════════════════════════════════════════════════════════════════════════════
WHERE TO FIND "CONNECT" BUTTON:
═══════════════════════════════════════════════════════════════════════════════

In your screenshot, you're viewing the Databases list.
For database "database-MH910T3P":

Option 1: Direct Click
  • Look in the row for "database-MH910T3P"
  • Find the "Connect" button in that row
  • Click it

Option 2: Click Database Name
  • Click on "database-MH910T3P" name
  • This should open database details
  • Look for "Connect" or "Connection" section

Option 3: Right Panel (You might see it already!)
  • On the right, there's a panel: "Connect to database-MH910T3P"
  • Look for dropdown menus
  • Select "Redis CLI" or "Connection String"
  • You should see your URL there!

═══════════════════════════════════════════════════════════════════════════════
QUICK STEPS:
═══════════════════════════════════════════════════════════════════════════════

1. In Redis Cloud Console (where you are now)
2. Look for "Connect" button for database-MH910T3P
3. Click it
4. Select "Redis CLI" option
5. Copy the connection string shown
6. It will look like: redis://:PASSWORD@redis-11022...
7. Share it with me (don't share the actual password - I just need the format)

═══════════════════════════════════════════════════════════════════════════════
WHAT YOU'LL SEE:
═══════════════════════════════════════════════════════════════════════════════

The Redis Cloud Console will show:

┌─────────────────────────────────────────────────────┐
│ Connect to database-MH910T3P                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Choose connection method:                           │
│ [Redis Insight ▼]  [Redis CLI ▼]  [Redis Client ▼]│
│                                                     │
│ Connection string:                                  │
│ redis://:YOUR_PASSWORD@redis-11022.c13...         │
│ [Copy button]                                       │
│                                                     │
└─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
COPY & SHARE FORMAT:
═══════════════════════════════════════════════════════════════════════════════

Once you have it, just tell me:

"My Redis connection string is: redis://:myPassword123@redis-11022.c13.us-east-1-3.ec2.redns.redis-cloud.com:11022"

(Replace myPassword123 with your actual password - but that's fine to share with me)

═══════════════════════════════════════════════════════════════════════════════
THEN I WILL:
═══════════════════════════════════════════════════════════════════════════════

1. ✅ Add it to your .env file (development)
2. ✅ Run test to verify it works
3. ✅ Show you how to add to Vercel/Render (production)
4. ✅ Complete your Redis setup!

═══════════════════════════════════════════════════════════════════════════════
STILL NEED THE RAZORPAY SECRET:
═══════════════════════════════════════════════════════════════════════════════

Also, we still need RAZORPAY_KEY_SECRET for payments to work.

Do you have it? If not:
1. Go to https://dashboard.razorpay.com/
2. Login
3. Settings → API Keys
4. Copy "Key Secret"
5. Add to .env: RAZORPAY_KEY_SECRET=your_secret_here

═══════════════════════════════════════════════════════════════════════════════

READY? Go to Redis Cloud and get your connection string! 🚀

═══════════════════════════════════════════════════════════════════════════════
