# 🚀 REDEPLOY INSTRUCTIONS FOR RENDER

## How to Force Redeploy Render Backend

Since the fix is already pushed to GitHub, we need to trigger a manual redeploy on Render:

### Steps:

1. **Go to:** https://dashboard.render.com
2. **Login** with your credentials
3. **Click** on your backend service (trulyinvoice-backend)
4. **Click** the "Manual Deploy" button or "Redeploy latest commit"
5. **Wait** 3-5 minutes for deployment
6. **Test** the eye icon on https://trulyinvoice.xyz/invoices

---

## What Was Fixed

The Supabase helper was over-encoding UUID hyphens in TWO places:

1. ✅ Fixed in `select()` method
2. ✅ Fixed in `query()` method (just added)

Now UUIDs like `8a56ccec-d4fa-46b1-ad20-9e8db71de2d7` will:
- ❌ NOT be converted to: `8a56ccec%2Dd4fa%2D46b1%2Dad20%2D9e8db71de2d7`
- ✅ STAY as: `8a56ccec-d4fa-46b1-ad20-9e8db71de2d7`

This allows Supabase to match the UUID correctly!

---

## Expected Result After Redeploy

Click eye icon → Invoice detail page loads ✅

No more 404 error!
