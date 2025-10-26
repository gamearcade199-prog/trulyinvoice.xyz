# 🚀 UPGRADE MODAL IMPLEMENTATION GUIDE
## How to Integrate Quota Limits and Upgrade Popups

**Created:** October 22, 2025  
**Status:** ✅ Components Created - Ready for Integration

---

## 📦 NEW COMPONENTS CREATED

### 1. ✅ UpgradeModal Component
**Location:** `frontend/src/components/UpgradeModal.tsx`

**Features:**
- ✅ Beautiful modal with gradient header
- ✅ Shows current usage (X/Y scans used)
- ✅ Displays available upgrade plans
- ✅ Highlights recommended plan
- ✅ Direct navigation to pricing page
- ✅ Responsive design (mobile & desktop)
- ✅ Dark mode support

**Props:**
```typescript
{
  isOpen: boolean
  onClose: () => void
  currentPlan: string
  scansUsed: number
  scansLimit: number
  reason: 'quota_exceeded' | 'feature_locked' | 'proactive_warning'
}
```

---

### 2. ✅ UsageWarning Component
**Location:** `frontend/src/components/UsageWarning.tsx`

**Features:**
- ✅ Shows warning at 80% usage (yellow)
- ✅ Shows urgent alert at 90% usage (red)
- ✅ Progress bar visualization
- ✅ Quick upgrade button
- ✅ Recommended plan suggestion
- ✅ Auto-hides below 80%

**Props:**
```typescript
{
  scansUsed: number
  scansLimit: number
  currentPlan: string
  onUpgradeClick?: () => void
}
```

---

### 3. ✅ useQuotaModal Hook
**Location:** `frontend/src/hooks/useQuotaModal.ts`

**Features:**
- ✅ Manages modal state
- ✅ Handles quota exceeded errors (HTTP 429)
- ✅ Parses error messages
- ✅ Custom error class
- ✅ Helper functions

**Usage:**
```typescript
const { 
  isModalOpen, 
  showUpgradeModal, 
  hideUpgradeModal, 
  handleQuotaError 
} = useQuotaModal()
```

---

## 🔧 INTEGRATION STEPS

### Step 1: Add to Homepage Upload
**File:** `frontend/src/components/HomePage.tsx`

```typescript
import UpgradeModal from '@/components/UpgradeModal'
import { useQuotaModal } from '@/hooks/useQuotaModal'

export default function HomePage() {
  const { 
    isModalOpen, 
    showUpgradeModal, 
    hideUpgradeModal, 
    handleQuotaError,
    quotaState 
  } = useQuotaModal()

  const handleUpload = async (file: File) => {
    try {
      const result = await uploadInvoiceAnonymous(file)
      // ... success handling
    } catch (error) {
      // ✅ Check if it's a quota error
      if (handleQuotaError(error)) {
        // Modal will automatically open
        return
      }
      // Handle other errors
      setError(error.message)
    }
  }

  return (
    <>
      {/* Your existing homepage content */}
      
      {/* ✅ Add Upgrade Modal */}
      <UpgradeModal
        isOpen={isModalOpen}
        onClose={hideUpgradeModal}
        currentPlan={quotaState?.currentPlan || 'free'}
        scansUsed={quotaState?.scansUsed || 0}
        scansLimit={quotaState?.scansLimit || 10}
        reason="quota_exceeded"
      />
    </>
  )
}
```

---

### Step 2: Add to Dashboard
**File:** `frontend/src/components/BillingDashboard.tsx`

```typescript
import UsageWarning from '@/components/UsageWarning'
import UpgradeModal from '@/components/UpgradeModal'
import { useQuotaModal } from '@/hooks/useQuotaModal'

export default function BillingDashboard() {
  const { isModalOpen, showUpgradeModal, hideUpgradeModal } = useQuotaModal()

  // Get subscription data (you already have this)
  const scansUsed = subscription?.scans_used_this_period || 0
  const scansLimit = planDetails[subscription?.tier]?.scans || 10
  const currentPlan = subscription?.tier || 'free'

  return (
    <div>
      {/* ✅ Add Usage Warning at top */}
      <UsageWarning
        scansUsed={scansUsed}
        scansLimit={scansLimit}
        currentPlan={currentPlan}
        onUpgradeClick={() => showUpgradeModal('proactive_warning')}
      />

      {/* Your existing dashboard content */}

      {/* ✅ Add Upgrade Modal */}
      <UpgradeModal
        isOpen={isModalOpen}
        onClose={hideUpgradeModal}
        currentPlan={currentPlan}
        scansUsed={scansUsed}
        scansLimit={scansLimit}
        reason="proactive_warning"
      />
    </div>
  )
}
```

---

### Step 3: Add to Invoice Upload Page
**File:** `frontend/src/app/invoices/page.tsx` (or wherever invoices are uploaded)

```typescript
import UpgradeModal from '@/components/UpgradeModal'
import UsageWarning from '@/components/UsageWarning'
import { useQuotaModal } from '@/hooks/useQuotaModal'

export default function InvoicesPage() {
  const [subscription, setSubscription] = useState(null)
  const { isModalOpen, showUpgradeModal, hideUpgradeModal, handleQuotaError } = useQuotaModal()

  // Fetch subscription data
  useEffect(() => {
    fetchSubscription()
  }, [])

  const handleFileUpload = async (file: File) => {
    try {
      // Call your upload API
      const response = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        if (response.status === 429) {
          // ✅ Quota exceeded
          const error = await response.json()
          handleQuotaError({ status: 429, detail: error.detail })
          return
        }
        throw new Error('Upload failed')
      }

      // Success
      const data = await response.json()
      // ... handle success
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div>
      {/* ✅ Show warning banner */}
      <UsageWarning
        scansUsed={subscription?.scans_used_this_period || 0}
        scansLimit={subscription?.scans_limit || 10}
        currentPlan={subscription?.tier || 'free'}
        onUpgradeClick={() => showUpgradeModal('proactive_warning')}
      />

      {/* Your upload UI */}
      <UploadZone onFileSelect={handleFileUpload} />

      {/* ✅ Upgrade modal */}
      <UpgradeModal
        isOpen={isModalOpen}
        onClose={hideUpgradeModal}
        currentPlan={subscription?.tier || 'free'}
        scansUsed={subscription?.scans_used_this_period || 0}
        scansLimit={subscription?.scans_limit || 10}
        reason="quota_exceeded"
      />
    </div>
  )
}
```

---

### Step 4: Update API Error Handling
**File:** `frontend/src/lib/invoiceUpload.ts`

```typescript
import { QuotaExceededError, isQuotaError } from '@/hooks/useQuotaModal'

export async function uploadInvoice(file: File) {
  try {
    const response = await fetch('/api/documents/upload', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      if (response.status === 429) {
        // ✅ Parse quota info from error
        const errorData = await response.json()
        const match = errorData.detail?.match(/Used: (\d+)\/(\d+)/)
        
        if (match) {
          throw new QuotaExceededError(
            errorData.detail,
            parseInt(match[1], 10),
            parseInt(match[2], 10)
          )
        }
        
        throw new QuotaExceededError(errorData.detail)
      }
      
      throw new Error('Upload failed')
    }

    return await response.json()
  } catch (error) {
    // ✅ Check if quota error
    if (isQuotaError(error)) {
      // Let the component handle it
      throw error
    }
    
    // Other errors
    console.error('Upload error:', error)
    throw error
  }
}
```

---

## 🎨 VISUAL EXAMPLES

### Quota Exceeded Modal
```
┌────────────────────────────────────────────────┐
│  🚀 Upgrade to Continue Processing            │
│  You've used all 10 scans this month.         │
│  [Current: free • 10/10 scans used]           │
├────────────────────────────────────────────────┤
│  Choose Your New Plan                          │
│                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Basic    │  │ Pro      │  │ Ultra    │   │
│  │ ₹149/mo  │  │ ₹299/mo  │  │ ₹599/mo  │   │
│  │ 80 scans │  │ 200 scans│  │ 500 scans│   │
│  │ [Upgrade]│  │ [Upgrade]│  │ [Upgrade]│   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                                │
│  [View All Plans →]                           │
├────────────────────────────────────────────────┤
│  ✅ Instant activation • 💳 Secure payment    │
│                          [Maybe Later]         │
└────────────────────────────────────────────────┘
```

### Usage Warning (80%)
```
┌────────────────────────────────────────────┐
│  ⚠️  Running low on scans                 │
│  You've used 8 of 10 scans this month.    │
│  [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░]│
│  [🚀 View Plans]  [View Usage]            │
└────────────────────────────────────────────┘
```

### Usage Warning (90%)
```
┌────────────────────────────────────────────┐
│  🚨 Last scan remaining!                   │
│  You have only 1 scan left on free plan.  │
│  [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━]│
│  [⚡ Upgrade Now]  [View Usage]           │
│  💡 Recommended: Upgrade to Basic (₹149/mo)│
└────────────────────────────────────────────┘
```

---

## ✅ TESTING CHECKLIST

### Scenario 1: User Hits Limit
- [ ] Upload 10 invoices on free plan
- [ ] Try to upload 11th invoice
- [ ] Verify HTTP 429 returned from backend
- [ ] **Verify upgrade modal appears**
- [ ] Click "Upgrade to Basic Plan"
- [ ] Verify redirects to `/pricing?plan=basic&upgrade=true`

### Scenario 2: Proactive Warning
- [ ] Upload 8 invoices (80%)
- [ ] **Verify yellow warning banner appears**
- [ ] Upload 9 invoices (90%)
- [ ] **Verify red urgent alert appears**
- [ ] Click "Upgrade Now"
- [ ] Verify modal opens

### Scenario 3: Upgrade Flow
- [ ] Click upgrade button in modal
- [ ] Complete payment
- [ ] Verify tier changes in database
- [ ] Verify limit increases immediately
- [ ] Verify can upload more invoices

### Scenario 4: Warning Disappears
- [ ] Have 5/10 scans used (50%)
- [ ] **Verify no warning shows**
- [ ] Upload to reach 8/10 (80%)
- [ ] **Verify warning appears**

---

## 🚀 DEPLOYMENT CHECKLIST

- [x] ✅ UpgradeModal component created
- [x] ✅ UsageWarning component created
- [x] ✅ useQuotaModal hook created
- [ ] Integrate modal in HomePage
- [ ] Integrate warning in Dashboard
- [ ] Integrate in Invoice Upload page
- [ ] Update API error handling
- [ ] Test all scenarios
- [ ] Deploy to production

---

## 📊 EXPECTED IMPACT

**Before:**
- ❌ Users hit limit and see generic error
- ❌ No clear path to upgrade
- ❌ Confusion and frustration
- ❌ Lost revenue

**After:**
- ✅ Beautiful upgrade modal appears
- ✅ Clear upgrade options shown
- ✅ One-click navigation to pricing
- ✅ Proactive warnings before limit
- ✅ Better user experience
- ✅ Increased conversions

---

## 💡 ADDITIONAL RECOMMENDATIONS

### 1. Analytics Tracking
```typescript
// Track when modal is shown
trackEvent('upgrade_modal_shown', {
  reason: 'quota_exceeded',
  current_plan: 'free',
  scans_used: 10
})

// Track when user clicks upgrade
trackEvent('upgrade_button_clicked', {
  target_plan: 'basic',
  source: 'quota_modal'
})
```

### 2. A/B Testing
Test different modal designs:
- Variant A: Show all plans
- Variant B: Show only recommended plan
- Measure conversion rate

### 3. Email Follow-up
When user hits limit:
- Send email: "You've reached your limit"
- Include upgrade link
- Offer discount code

### 4. Gradual Warnings
- 50% usage: Subtle notification
- 80% usage: Yellow warning
- 90% usage: Red alert
- 100% usage: Block with modal

---

## 📝 CODE SNIPPETS

### Quick Integration (Copy-Paste)
```typescript
// 1. Import components
import UpgradeModal from '@/components/UpgradeModal'
import UsageWarning from '@/components/UsageWarning'
import { useQuotaModal } from '@/hooks/useQuotaModal'

// 2. Initialize hook
const { isModalOpen, showUpgradeModal, hideUpgradeModal, handleQuotaError } = useQuotaModal()

// 3. Add warning (optional)
<UsageWarning
  scansUsed={scansUsed}
  scansLimit={scansLimit}
  currentPlan={currentPlan}
  onUpgradeClick={() => showUpgradeModal('proactive_warning')}
/>

// 4. Add modal
<UpgradeModal
  isOpen={isModalOpen}
  onClose={hideUpgradeModal}
  currentPlan={currentPlan}
  scansUsed={scansUsed}
  scansLimit={scansLimit}
  reason="quota_exceeded"
/>

// 5. Handle errors
catch (error) {
  if (handleQuotaError(error)) {
    return // Modal will open automatically
  }
  // Handle other errors
}
```

---

## 🎯 SUCCESS METRICS

Track these after deployment:

1. **Modal Show Rate**
   - How many users see the modal?
   
2. **Click-Through Rate**
   - % who click "Upgrade Now"

3. **Conversion Rate**
   - % who complete payment

4. **Time to Upgrade**
   - How quickly users upgrade after hitting limit

5. **Churn Prevention**
   - % of users who return after hitting limit

---

**Status:** Ready for Integration  
**Next Step:** Integrate components into existing pages  
**Priority:** HIGH - Directly impacts revenue
