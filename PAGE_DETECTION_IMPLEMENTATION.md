# PDF Page Detection Implementation Guide

## ✅ Step 1: Install Package (DONE)
```bash
npm install pdf-lib
```

## ✅ Step 2: Utility Created
File: `frontend/src/utils/pdfPageCounter.ts`

## 📋 Step 3: Add to Upload Page

### Add these imports at the top:
```typescript
import { getTotalPageCount, getMultipleFilePageCounts } from '@/utils/pdfPageCounter'
```

### Replace PLAN_BATCH_LIMITS with HYBRID limits:
```typescript
// Plan-based HYBRID limits (files + pages)
const PLAN_LIMITS = {
  'Free': { files: 1, pagesPerMonth: 10 },
  'Basic': { files: 5, pagesPerMonth: 100 },
  'Pro': { files: 10, pagesPerMonth: 500 },
  'Ultra': { files: 50, pagesPerMonth: 2000 },
  'Max': { files: 100, pagesPerMonth: 10000 },
}
```

### Add state for page tracking:
```typescript
const [totalPages, setTotalPages] = useState(0)
const [pageDetails, setPageDetails] = useState<{fileName: string, pageCount: number}[]>([])
```

### Update handleFileSelect to count pages:
```typescript
const handleFileSelect = async (selectedFiles: File[]) => {
  setFiles(selectedFiles)
  setUploadComplete(false)
  setError('')
  setProcessingStatus('Analyzing files...')
  
  // Count pages in all files
  try {
    const pageInfo = await getMultipleFilePageCounts(selectedFiles)
    const total = pageInfo.reduce((sum, info) => sum + info.pageCount, 0)
    
    setTotalPages(total)
    setPageDetails(pageInfo.map(info => ({
      fileName: info.fileName,
      pageCount: info.pageCount
    })))
    
    setProcessingStatus(`✅ ${selectedFiles.length} files, ${total} total pages`)
  } catch (error) {
    console.error('Error analyzing files:', error)
    setTotalPages(selectedFiles.length) // Fallback: assume 1 page per file
  }
  
  setAnonymousResult(null)
  setShowAnonymousModal(false)
}
```

### Update validation in handleUpload:
```typescript
// Inside handleUpload, replace the batch limit check with:

const userPlan = userData?.plan || 'Free'
const planLimits = PLAN_LIMITS[userPlan] || PLAN_LIMITS['Free']

console.log(`📊 User plan: ${userPlan}`)
console.log(`📄 Files: ${files.length}/${planLimits.files}`)
console.log(`📃 Pages: ${totalPages}`)

// Check file count limit
if (files.length > planLimits.files) {
  setError(`❌ Your ${userPlan} plan allows ${planLimits.files} files per batch. You selected ${files.length} files. Please upgrade or reduce files.`)
  setIsUploading(false)
  return
}

// Check if user has enough page quota (requires pages_used column in users table)
const { data: usageData } = await supabase
  .from('users')
  .select('pages_used_this_month, billing_period_start')
  .eq('id', user.id)
  .single()

const pagesUsed = usageData?.pages_used_this_month || 0
const pagesRemaining = planLimits.pagesPerMonth - pagesUsed

if (totalPages > pagesRemaining) {
  setError(`❌ Not enough page quota! You have ${pagesRemaining} pages remaining this month. These files contain ${totalPages} pages. Upgrade your plan or wait for next billing cycle.`)
  setIsUploading(false)
  return
}

console.log(`✅ Quota check passed: ${totalPages} pages, ${pagesRemaining} remaining`)
```

### After successful processing, update pages_used:
```typescript
// After all files are processed successfully, update usage:
await supabase
  .from('users')
  .update({ 
    pages_used_this_month: pagesUsed + totalPages 
  })
  .eq('id', user.id)

console.log(`📊 Updated usage: ${pagesUsed} -> ${pagesUsed + totalPages} pages`)
```

## 📊 Step 4: Database Changes Needed

Add to users table:
```sql
ALTER TABLE users 
ADD COLUMN pages_used_this_month INTEGER DEFAULT 0,
ADD COLUMN billing_period_start TIMESTAMP DEFAULT NOW();

-- Create function to reset monthly usage
CREATE OR REPLACE FUNCTION reset_monthly_page_usage()
RETURNS void AS $$
BEGIN
  UPDATE users 
  SET pages_used_this_month = 0,
      billing_period_start = NOW()
  WHERE billing_period_start < NOW() - INTERVAL '1 month';
END;
$$ LANGUAGE plpgsql;

-- Schedule monthly reset (run via cron or manually)
-- SELECT reset_monthly_page_usage();
```

## 🎨 Step 5: UI Display

Add page count display in the upload zone:
```typescript
{pageDetails.length > 0 && (
  <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
    <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
      📊 File Analysis
    </h4>
    <div className="space-y-1 text-sm text-blue-800 dark:text-blue-200">
      {pageDetails.map((detail, idx) => (
        <div key={idx}>
          {detail.fileName}: <strong>{detail.pageCount} pages</strong>
        </div>
      ))}
      <div className="mt-2 pt-2 border-t border-blue-200 dark:border-blue-700 font-bold">
        Total: {files.length} files, {totalPages} pages
      </div>
    </div>
  </div>
)}
```

## 📈 Benefits

### Before (File-based only):
- ❌ User merges 100 invoices into 1 PDF → Only counts as 1 file
- ❌ Unfair for users who upload separate files
- ❌ High API costs for merged PDFs

### After (Hybrid File + Page):
- ✅ 1 file with 100 pages = 100 pages counted
- ✅ 100 files with 1 page each = 100 pages counted
- ✅ Fair pricing based on actual processing cost
- ✅ Monthly page quota prevents abuse
- ✅ Users see exactly what they're using

## 🚀 Implementation Priority

**Phase 1 (Quick - 20 mins):**
- ✅ Install pdf-lib
- ✅ Create pdfPageCounter.ts utility
- Add page detection to handleFileSelect
- Display page counts in UI

**Phase 2 (Database - 30 mins):**
- Add pages_used_this_month column
- Add billing_period_start column
- Create reset function
- Add validation in handleUpload

**Phase 3 (Admin - 15 mins):**
- Show page usage in admin panel
- Add manual reset button
- Display usage statistics

Total time: ~65 minutes for complete implementation

## 🎯 Recommended Plan Limits

```typescript
const PLAN_LIMITS = {
  'Free': { 
    files: 1,           // 1 file per upload
    pagesPerMonth: 10   // 10 pages per month
  },
  'Basic': { 
    files: 5,           // 5 files per upload
    pagesPerMonth: 100  // 100 pages per month (~$2-3 in API costs)
  },
  'Pro': { 
    files: 10,          // 10 files per upload  
    pagesPerMonth: 500  // 500 pages per month (~$10-15 in API costs)
  },
  'Ultra': { 
    files: 50,          // 50 files per upload
    pagesPerMonth: 2000 // 2000 pages per month (~$40-60 in API costs)
  },
  'Max': { 
    files: 100,         // 100 files per upload
    pagesPerMonth: 10000 // 10000 pages per month (~$200-300 in API costs)
  },
}
```

## 🔥 Quick Implementation

Want me to implement this now? Just say:
- "implement phase 1" → Add page detection & UI (20 min)
- "implement phase 2" → Add database tracking (30 min)  
- "implement all" → Full hybrid system (65 min)
