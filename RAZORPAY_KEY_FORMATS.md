# 🔑 Razorpay API Keys Format Guide

## 📋 Razorpay Key Formats

### **1. Key ID (RAZORPAY_KEY_ID)**

#### Test Mode:
```
rzp_test_xxxxxxxxxxxx
```
- Starts with: `rzp_test_`
- Followed by: 16 alphanumeric characters
- Length: ~25 characters total
- Example: `rzp_test_1A2B3C4D5E6F7G8H`

#### Live Mode (Production):
```
rzp_live_xxxxxxxxxxxx
```
- Starts with: `rzp_live_`
- Followed by: 16 alphanumeric characters
- Length: ~25 characters total
- Example: `rzp_live_9Z8Y7X6W5V4U3T2S`

---

### **2. Key Secret (RAZORPAY_KEY_SECRET)**

#### Format:
```
xxxxxxxxxxxxxxxxxxxxxxxx
```
- Pure alphanumeric string
- No prefix
- Length: ~24 characters
- Case-sensitive
- Mix of uppercase and lowercase
- Example: `AbCdEf1234GhIjKl5678MnOp`

---

### **3. Webhook Secret (RAZORPAY_WEBHOOK_SECRET)**

#### Format:
```
xxxxxxxxxxxxxxxxxxxxxxxx
```
- Pure alphanumeric string
- No prefix
- Length: ~24-32 characters
- Case-sensitive
- Generated when you create a webhook
- Example: `WhSec1234AbCd5678EfGh9012`

---

## 🎯 Complete Example

### Test Environment (.env):
```bash
RAZORPAY_KEY_ID=rzp_test_1A2B3C4D5E6F7G8H
RAZORPAY_KEY_SECRET=AbCdEf1234GhIjKl5678MnOp
RAZORPAY_WEBHOOK_SECRET=WhSec1234AbCd5678EfGh9012
```

### Production Environment (.env):
```bash
RAZORPAY_KEY_ID=rzp_live_9Z8Y7X6W5V4U3T2S
RAZORPAY_KEY_SECRET=XyZaBc9876DeFgHi5432JkLm
RAZORPAY_WEBHOOK_SECRET=WhSec9876ZyXw5432VuTs1234
```

---

## 📍 Where to Find Each Key

### **Key ID & Key Secret:**

1. **Login to Razorpay Dashboard**
   - URL: https://dashboard.razorpay.com

2. **Navigate to API Keys**
   - Settings → API Keys
   - Or direct: https://dashboard.razorpay.com/app/keys

3. **Generate Keys**
   - Click "Generate Test Keys" for testing
   - Click "Generate Live Keys" for production
   - You'll see both Key ID and Key Secret

4. **Copy Both Keys**
   ```
   Key ID:     rzp_test_1A2B3C4D5E6F7G8H
   Key Secret: AbCdEf1234GhIjKl5678MnOp
   ```

---

### **Webhook Secret:**

1. **Navigate to Webhooks**
   - Settings → Webhooks
   - Or: https://dashboard.razorpay.com/app/webhooks

2. **Add New Webhook**
   - Click "Add New Webhook"
   - Enter webhook URL: `https://your-backend.com/api/payments/webhook`

3. **Select Events**
   - ✅ payment.authorized
   - ✅ payment.captured
   - ✅ payment.failed

4. **Get Webhook Secret**
   - After creating, click on the webhook
   - Click "Show Secret"
   - Copy the secret
   ```
   Webhook Secret: WhSec1234AbCd5678EfGh9012
   ```

---

## ✅ Validation Checklist

### **Valid Key ID:**
- [ ] Starts with `rzp_test_` or `rzp_live_`
- [ ] Contains 16 alphanumeric characters after prefix
- [ ] Total length: ~25 characters
- [ ] No spaces or special characters

### **Valid Key Secret:**
- [ ] Pure alphanumeric (no prefix)
- [ ] Length: ~24 characters
- [ ] Mix of uppercase and lowercase
- [ ] No spaces or special characters

### **Valid Webhook Secret:**
- [ ] Pure alphanumeric (no prefix)
- [ ] Length: ~24-32 characters
- [ ] Case-sensitive
- [ ] No spaces or special characters

---

## ⚠️ Common Mistakes

### ❌ **Wrong:**
```bash
# Missing prefix
RAZORPAY_KEY_ID=1A2B3C4D5E6F7G8H

# Extra quotes
RAZORPAY_KEY_SECRET="AbCdEf1234GhIjKl5678MnOp"

# Spaces
RAZORPAY_KEY_ID=rzp_test_1A2B 3C4D 5E6F7G8H

# Wrong prefix
RAZORPAY_KEY_ID=razorpay_test_1A2B3C4D5E6F7G8H
```

### ✅ **Correct:**
```bash
RAZORPAY_KEY_ID=rzp_test_1A2B3C4D5E6F7G8H
RAZORPAY_KEY_SECRET=AbCdEf1234GhIjKl5678MnOp
RAZORPAY_WEBHOOK_SECRET=WhSec1234AbCd5678EfGh9012
```

---

## 🧪 Testing Your Keys

### **Test if Keys are Valid:**

#### Method 1: Using cURL
```bash
curl -u rzp_test_1A2B3C4D5E6F7G8H:AbCdEf1234GhIjKl5678MnOp \
  https://api.razorpay.com/v1/payments
```

If valid, you'll get a JSON response. If invalid, you'll get 401 error.

#### Method 2: In Your Backend
```python
# In your FastAPI backend
import razorpay

client = razorpay.Client(
    auth=("rzp_test_1A2B3C4D5E6F7G8H", "AbCdEf1234GhIjKl5678MnOp")
)

# Test connection
try:
    orders = client.order.all()
    print("✅ Keys are valid!")
except Exception as e:
    print(f"❌ Invalid keys: {e}")
```

---

## 📝 Sample .env File

```bash
# ==============================================
# RAZORPAY PAYMENT GATEWAY
# ==============================================

# Test Mode (Development)
RAZORPAY_KEY_ID=rzp_test_1A2B3C4D5E6F7G8H
RAZORPAY_KEY_SECRET=AbCdEf1234GhIjKl5678MnOp
RAZORPAY_WEBHOOK_SECRET=WhSec1234AbCd5678EfGh9012

# Live Mode (Production - Uncomment when going live)
# RAZORPAY_KEY_ID=rzp_live_9Z8Y7X6W5V4U3T2S
# RAZORPAY_KEY_SECRET=XyZaBc9876DeFgHi5432JkLm
# RAZORPAY_WEBHOOK_SECRET=WhSec9876ZyXw5432VuTs1234
```

---

## 🔄 Test Mode vs Live Mode

### **Test Mode** (Development):
- Key ID starts with: `rzp_test_`
- Use for development and testing
- No real money is charged
- Can use test cards (4111 1111 1111 1111)
- Free to use

### **Live Mode** (Production):
- Key ID starts with: `rzp_live_`
- Use for production
- Real money transactions
- Must have KYC completed
- Standard Razorpay fees apply (~2%)

---

## 🔐 Security Best Practices

### **DO:**
✅ Store keys in environment variables
✅ Never commit keys to Git
✅ Use test keys for development
✅ Regenerate keys if exposed
✅ Keep Key Secret hidden (backend only)
✅ Use different keys for each environment

### **DON'T:**
❌ Share keys publicly
❌ Hardcode in source code
❌ Use live keys in development
❌ Expose Key Secret in frontend
❌ Commit .env file to repository

---

## 📞 Support

- **Get Keys**: https://dashboard.razorpay.com/app/keys
- **Webhooks**: https://dashboard.razorpay.com/app/webhooks
- **Docs**: https://razorpay.com/docs/api
- **Test Cards**: https://razorpay.com/docs/payments/payments/test-card-upi-details/

---

## ✅ Quick Validation Script

Save this as `test_razorpay_keys.py`:

```python
import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

print(f"Testing Razorpay Keys...")
print(f"Key ID: {key_id}")
print(f"Key Secret: {'*' * len(key_secret)}")

try:
    client = razorpay.Client(auth=(key_id, key_secret))
    orders = client.order.all()
    print("\n✅ SUCCESS! Your Razorpay keys are valid!")
    print(f"Found {len(orders['items'])} orders in your account.")
except razorpay.errors.BadRequestError as e:
    print(f"\n❌ ERROR: {e}")
    print("Please check your keys and try again.")
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")
```

Run it:
```bash
python test_razorpay_keys.py
```

---

**Need help getting your keys? Check the Razorpay dashboard!** 🚀
