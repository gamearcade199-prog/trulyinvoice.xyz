# 📅 BILLING CYCLE VISUAL EXPLANATION

## Your Question:
> "If user buys plan at 15th March and uses all scans in March,  
> will the scans limit reset on 1st April?"

---

## ⚠️ ANSWER: **NO - Resets on 15th April**

---

## 📊 Visual Timeline

```
MARCH 2025                          APRIL 2025
┌──────────────────────────────────┬──────────────────────────────────┐
│  1  2  3  4  5  6  7  8  9  10   │  1  2  3  4  5  6  7  8  9  10   │
│ 11 12 13 14 [15]16 17 18 19 20   │ 11 12 13 14 [15]16 17 18 19 20   │
│ 21 22 23 24 25 26 27 28 29 30 31 │ 21 22 23 24 25 26 27 28 29 30    │
└──────────────────────────────────┴──────────────────────────────────┘
                ▲                                  ▲
            March 15                            April 15
         🎉 PURCHASED                        ✅ RESETS HERE
         500 pages                          (not April 1st!)
```

---

## 📖 Story of User "John"

### ✅ Correct Understanding:

```
📅 March 15, 2025 - 10:00 AM
┌─────────────────────────────────────┐
│ John buys Pro Plan                  │
│ • 500 pages/month                   │
│ • billing_period_start: March 15    │
│ • pages_used: 0                     │
└─────────────────────────────────────┘

📅 March 20, 2025 - 3:00 PM
┌─────────────────────────────────────┐
│ John uploads 100 invoices           │
│ • 500 pages total                   │
│ • pages_used: 500 ❌ ALL USED       │
└─────────────────────────────────────┘

📅 April 1, 2025 - 9:00 AM
┌─────────────────────────────────────┐
│ John tries to upload                │
│ ❌ BLOCKED!                          │
│ Reason: Only 17 days passed         │
│ (Need 1 full month = 30+ days)      │
└─────────────────────────────────────┘

📅 April 10, 2025 - 2:00 PM
┌─────────────────────────────────────┐
│ John tries again                    │
│ ❌ STILL BLOCKED!                    │
│ Reason: Only 26 days passed         │
└─────────────────────────────────────┘

📅 April 15, 2025 - 10:01 AM
┌─────────────────────────────────────┐
│ John uploads new invoice            │
│ ✅ SUCCESS!                          │
│ • 1 month passed ✅                  │
│ • pages_used: 0 (reset)             │
│ • billing_period_start: April 15    │
│ • New 500-page quota unlocked       │
└─────────────────────────────────────┘
```

---

## ❌ Common Misconception

### What People Think:

```
❌ WRONG ASSUMPTION:
"Billing resets on 1st of every month"

March:  Purchase on 15th → Use 500 pages
April:  Reset on 1st → Get 500 new pages ❌

This is NOT how it works!
```

### How It Actually Works:

```
✅ CORRECT LOGIC:
"Billing resets on PURCHASE ANNIVERSARY"

March:  Purchase on 15th → Use 500 pages
April:  Reset on 15th → Get 500 new pages ✅

Each cycle is EXACTLY 1 month from purchase date!
```

---

## 🔍 Why Anniversary-Based?

### Reason 1: **Fairness**
```
Calendar Reset:
- Buy March 31 → Only 1 day until April 1 reset ❌

Anniversary Reset:
- Buy March 31 → Full 30 days until March 31 reset ✅
```

### Reason 2: **Load Distribution**
```
Calendar Reset:
- Everyone resets April 1 → Server overload ❌

Anniversary Reset:
- Users reset on different days → Even load ✅
```

### Reason 3: **Simplicity**
```
Calendar Reset:
- Track: Purchase date, current month, last reset month
- Complex edge cases (month lengths, leap years)

Anniversary Reset:
- Track: Just billing_period_start
- Simple: months_passed >= 1? Reset!
```

---

## 🧮 Math Behind Reset

### SQL Logic:
```sql
-- How many months between two dates?
months_passed = EXTRACT(YEAR FROM AGE(now, start)) * 12 +
                EXTRACT(MONTH FROM AGE(now, start))

-- Examples:
March 15 → April 1:  AGE = 17 days  = 0 months  ❌ No reset
March 15 → April 14: AGE = 30 days  = 0 months  ❌ No reset
March 15 → April 15: AGE = 1 month  = 1 month   ✅ RESET!
March 15 → April 16: AGE = 32 days  = 1 month   ✅ RESET!
```

### Real Test Cases:

| Purchase Date | Current Date | Months | Reset? |
|---------------|--------------|--------|--------|
| Jan 31 | Feb 28 | 0 | ❌ |
| Jan 31 | Mar 1 | 1 | ✅ |
| Feb 28 | Mar 28 | 1 | ✅ |
| Feb 28 | Mar 27 | 0 | ❌ |
| Dec 15 | Jan 15 | 1 | ✅ |
| Dec 31 | Jan 1 | 0 | ❌ |

---

## 🎯 Key Takeaways

### 1️⃣ Reset is ANNIVERSARY-BASED
- Not calendar month (1st of month)
- Exactly 1 month from purchase date
- Example: March 15 → April 15

### 2️⃣ Reset is AUTOMATIC
- Checks on every upload
- No manual action needed
- Happens instantly when month passes

### 3️⃣ Reset is FAIR
- Full 30-day cycle for everyone
- No matter when you buy in month
- Pro-rated? No - full quota each cycle

### 4️⃣ Unused Quota DOESN'T CARRY OVER
- Use 100/500 pages in March
- April 15: Reset to 0/500 (not 400/500)
- Start fresh each cycle

---

## 💡 Pro Tips for Users

### Tip 1: Plan Your Usage
```
Buy on 15th of month
→ Heavy usage near month-end (30th-31st) is safe
→ Still have 15 days until reset
```

### Tip 2: Check Quota Before Large Batch
```
✅ Always check pages_remaining before upload
✅ System shows: "250/500 pages used"
✅ Plan large batches around reset date
```

### Tip 3: Understand "Month"
```
1 month = Calendar month difference, not 30 days

Jan 31 → Feb 28 = 1 month (28 days) ✅
Feb 1 → Feb 28 = 0 months (27 days) ❌
Feb 28 → Mar 28 = 1 month (28 days) ✅
```

---

## 🔧 Technical Implementation

### Where Reset Happens:
```typescript
// In upload/page.tsx (line ~142)
await supabase.rpc('check_and_reset_billing_period', {
  user_id_param: user.id
})

// SQL checks:
if (months_passed >= 1) {
  UPDATE users SET
    pages_used_this_month = 0,
    billing_period_start = NOW()  ← New cycle starts
  WHERE id = user_id;
}
```

### When It's Called:
- ✅ Every file upload (before quota check)
- ✅ Automatic, no cron job needed
- ✅ Instant reset when eligible

---

## 📞 User Support Scenarios

### Scenario 1: "Why can't I upload? It's April!"
**Answer:** Your billing cycle started March 15, so it resets April 15 (not April 1).

### Scenario 2: "I bought on March 31, only got 1 day?"
**Answer:** No - you get a full month. Reset is March 31 → April 30 (1 full month).

### Scenario 3: "Can I reset early by upgrading?"
**Answer:** Upgrading changes your limit but keeps your billing_period_start. Wait for anniversary.

### Scenario 4: "I have 100 pages left, can they carry over?"
**Answer:** No - quota resets to full amount (500) on your anniversary, unused pages don't carry over.

---

## ✅ FINAL ANSWER

### Question: 
> "User buys plan at 15th March and uses all scans in March,  
> will the scans limit reset on 1st April?"

### Answer:
# ❌ NO

### Correct Reset Date:
# ✅ April 15th
(Exactly 1 month after purchase)

---

**System:** Anniversary-based billing  
**Logic:** months_passed >= 1  
**Reset:** Automatic on first upload after 1 month  
**Fair:** Everyone gets full cycle regardless of purchase date  

🎉 **This is the better design!** 🎉
