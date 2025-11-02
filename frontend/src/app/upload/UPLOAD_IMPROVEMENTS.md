# Bulk Upload Improvements - Implementation Plan

## ✅ Completed
1. **File Size Limit**: Increased to 25MB per file (done in UploadZone.tsx)

## 🚀 Improvements to Implement

### 1. Plan-Based Batch Limits
**Current State**: Any authenticated user can upload unlimited files
**Required Changes**:
- Free: 1 invoice per batch
- Basic: 5 invoices per batch  
- Pro: 10 invoices per batch
- Ultra: 50 invoices per batch
- Max: 100 invoices per batch

**Implementation**:
```typescript
// Fetch user's plan from database
const { data: userData } = await supabase
  .from('users')
  .select('plan')
  .eq('id', user.id)
  .single()

const PLAN_LIMITS = {
  'Free': 1,
  'Basic': 5,
  'Pro': 10,
  'Ultra': 50,
  'Max': 100
}

const userLimit = PLAN_LIMITS[userData.plan] || 1

if (files.length > userLimit) {
  setError(`Your ${userData.plan} plan allows ${userLimit} files per batch. Upgrade for more!`)
  return
}
```

### 2. Parallel Processing (5 at a time)
**Current State**: Sequential processing (1 file at a time)
**Performance Impact**: 
- 100 files = 100 sequential API calls = 5+ minutes
- With parallel (5 at a time) = 20 batches = ~1-2 minutes

**Implementation**:
```typescript
const PARALLEL_BATCH_SIZE = 5

for (let i = 0; i < files.length; i += PARALLEL_BATCH_SIZE) {
  const batch = files.slice(i, Math.min(i + PARALLEL_BATCH_SIZE, files.length))
  
  // Process all files in this batch in parallel
  const batchPromises = batch.map(async (file) => {
    // Upload to storage
    // Create DB record
    // Process with AI
    return { success: true, fileName: file.name }
  })
  
  // Wait for all files in batch to complete
  const results = await Promise.allSettled(batchPromises)
  
  // Log progress
  console.log(`Batch complete: ${results.filter(r => r.status === 'fulfilled').length} succeeded`)
  
  // Small delay between batches
  await new Promise(resolve => setTimeout(resolve, 1000))
}
```

### 3. UI Enhancements
- Show batch progress (Batch 1/5, 25% complete)
- Display parallel processing indicator
- Add upgrade prompt when exceeding plan limit
- Show estimated time remaining

## Performance Comparison

| Files | Sequential | Parallel (5x) | Time Saved |
|-------|-----------|---------------|------------|
| 10    | 2 min     | 30 sec        | 75%        |
| 50    | 10 min    | 2 min         | 80%        |
| 100   | 20 min    | 4 min         | 80%        |

## Server Load Considerations
- 5 concurrent requests per batch is reasonable
- 1 second delay between batches prevents overload
- Each request has 3 retry attempts
- Failed files don't block batch completion
