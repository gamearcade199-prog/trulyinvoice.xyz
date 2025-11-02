# 🚀 IMMEDIATE ACTION ITEMS - Domain Update Checklist

## ⚡ DO THIS RIGHT NOW (Before Deploying)

### 1️⃣ ADD DOMAIN IN VERCEL (5 minutes)
**This is REQUIRED before deployment!**

```
🔗 Go to: https://vercel.com/dashboard
📁 Select: Your trulyinvoice project
⚙️  Click: Settings → Domains
➕ Click: Add Domain

Add these two domains:
1. trulyinvoice.com
2. www.trulyinvoice.com

Vercel will show you DNS records → COPY THEM!
```

---

### 2️⃣ CONFIGURE HOSTINGER DNS (10 minutes)
**Log into Hostinger:**

```
🔗 Go to: https://hostinger.com
📧 Login with your account
🌐 Go to: Domains section
⚙️  Click: Manage for trulyinvoice.com
📝 Click: DNS / Nameservers → Manage DNS records
```

**Add these DNS records:**

#### A Record (Root Domain):
```
Type: A
Name: @ (or leave empty)
Points to: 76.76.21.21
TTL: 3600
```

#### CNAME Record (WWW):
```
Type: CNAME
Name: www
Points to: cname.vercel-dns.com
TTL: 3600
```

**IMPORTANT:** 
- ❌ Delete any existing A records pointing to Hostinger's parking page
- ❌ Delete any conflicting CNAME records for www

---

### 3️⃣ BUILD & TEST LOCALLY (3 minutes)
```bash
cd frontend
npm run build
```

**Check for errors!** Fix any build errors before deploying.

**Test locally:**
```bash
npm run dev
```

**Open:** http://localhost:3000  
**Verify:** 
- ✅ Site loads without errors
- ✅ Open DevTools → Console → No red errors
- ✅ View Page Source → Check for "trulyinvoice.com" (not .xyz)

---

### 4️⃣ COMMIT & PUSH (2 minutes)
```bash
git add .
git commit -m "feat: migrate to trulyinvoice.com domain - update all SEO configs"
git push origin main
```

Vercel will automatically deploy!

---

### 5️⃣ WAIT FOR DNS PROPAGATION (5-30 minutes)
**Check DNS status:**
```
🔗 Go to: https://dnschecker.org
🔍 Enter: trulyinvoice.com
✅ Verify: A record shows 76.76.21.21
```

**Timeline:**
- 5-10 min: DNS typically propagates
- 30 min: Should be fully propagated
- 72 hours: Maximum time (rare)

---

### 6️⃣ VERIFY DOMAIN IN VERCEL (After DNS propagates)
```
🔗 Go to: Vercel Dashboard → Your Project → Domains
🔄 Click: Refresh next to trulyinvoice.com
✅ Status should change from "Pending" to "Verified"
🔒 SSL certificate will be auto-provisioned (5-10 min)
```

---

### 7️⃣ TEST YOUR LIVE SITE (Final check)
Once Vercel shows "Verified":

**Test URLs:**
```
✅ https://trulyinvoice.com
✅ https://www.trulyinvoice.com
```

**Verify SEO Tags:**
```
1. Right-click → View Page Source
2. Search for: "trulyinvoice.com"
3. Check these exist:
   ✅ <meta property="og:url" content="https://trulyinvoice.com"
   ✅ <link rel="canonical" href="https://trulyinvoice.com"
   ✅ "url": "https://trulyinvoice.com" (in JSON-LD script)
```

**Test Sitemap & Robots:**
```
✅ https://trulyinvoice.com/sitemap.xml
✅ https://trulyinvoice.com/robots.txt
```

---

## 🎯 QUICK REFERENCE

### Files Already Updated ✅
- ✅ frontend/src/config/seo.config.ts
- ✅ frontend/src/lib/metadata.ts
- ✅ frontend/src/app/sitemap.ts
- ✅ frontend/src/app/robots.ts
- ✅ frontend/src/app/layout.tsx
- ✅ frontend/next.config.js
- ✅ backend/app/main.py
- ✅ backend/app/core/config.py
- ✅ backend/app/middleware/security_headers.py
- ✅ All page files with metadata

### What You Need to Do 🎯
1. ☐ Add domain in Vercel
2. ☐ Configure DNS in Hostinger
3. ☐ Build locally (`npm run build`)
4. ☐ Commit & push to GitHub
5. ☐ Wait for DNS propagation
6. ☐ Verify in Vercel
7. ☐ Test live site

---

## 🆘 Troubleshooting

### DNS not propagating?
```
- Wait 30 minutes
- Check: https://dnschecker.org
- Verify: A record = 76.76.21.21
- Verify: No conflicting DNS records in Hostinger
```

### Vercel won't verify domain?
```
- Check DNS is propagated first
- Click "Refresh" button in Vercel
- Check for typos in DNS records
- Wait a bit longer (can take up to 1 hour)
```

### Site shows old .xyz URLs?
```
- Hard refresh browser: Ctrl+Shift+R (Win) / Cmd+Shift+R (Mac)
- Clear browser cache
- Check in incognito mode
- Verify build was successful
```

### SSL certificate not working?
```
- Wait 10 minutes after domain verification
- Vercel auto-provisions SSL (takes 5-10 min)
- Try accessing https://trulyinvoice.com again
```

---

## ✅ Success Indicators

You'll know everything is working when:
- ✅ https://trulyinvoice.com loads without errors
- ✅ https://www.trulyinvoice.com redirects to main domain
- ✅ SSL certificate shows as valid (🔒 in address bar)
- ✅ View Page Source shows "trulyinvoice.com" everywhere
- ✅ Sitemap accessible at /sitemap.xml
- ✅ Robots.txt accessible at /robots.txt
- ✅ No console errors in browser DevTools

---

## 🎉 You're Ready!

**Everything is updated to 10/10 for .com domain!**

Just follow the 7 steps above and you'll be live on your new domain in ~30 minutes.

**Good luck! 🚀**

---

**Created:** November 2, 2025  
**Status:** Ready to Deploy
