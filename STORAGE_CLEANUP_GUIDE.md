# 🗄️ STORAGE CLEANUP CRON JOB SETUP

## Overview
This guide explains how to set up automated storage cleanup based on subscription tiers.

## Storage Retention by Plan

Based on `backend/app/config/plans.py`:

| Plan | Storage Days | Description |
|------|-------------|-------------|
| Free | 1 day | Auto-delete after 24 hours |
| Basic | 7 days | Auto-delete after 1 week |
| Pro | 30 days | Auto-delete after 1 month |
| Ultra | 60 days | Auto-delete after 2 months |
| Max | 90 days | Auto-delete after 3 months |

## Cleanup Methods

### 1. Manual Cleanup (Command Line)

```bash
# From backend directory
cd backend

# Clean up all users
python -m app.services.storage_cleanup cleanup-all

# Clean up anonymous uploads only
python -m app.services.storage_cleanup cleanup-anonymous

# Get storage stats for a user
python -m app.services.storage_cleanup stats <user_id>
```

### 2. API Endpoints

```bash
# Clean up current user's data
POST /api/storage/cleanup/user
Headers: Authorization: Bearer <token>

# Get current user's storage stats
GET /api/storage/stats
Headers: Authorization: Bearer <token>

# Clean up all users (admin only)
POST /api/storage/cleanup/all

# Clean up anonymous uploads (admin only)
POST /api/storage/cleanup/anonymous
```

### 3. Automated Cron Jobs

#### Option A: Render.com Cron Jobs (Recommended for Render deployment)

1. Go to Render Dashboard
2. Create a new "Cron Job" service
3. Configure:
   - **Name**: `trulyinvoice-cleanup`
   - **Environment**: Same as backend
   - **Command**: `python -m app.services.storage_cleanup cleanup-all && python -m app.services.storage_cleanup cleanup-anonymous`
   - **Schedule**: `0 2 * * *` (Daily at 2 AM UTC)

#### Option B: GitHub Actions (Free, works anywhere)

Create `.github/workflows/cleanup.yml`:

```yaml
name: Daily Storage Cleanup

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  cleanup:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run cleanup
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
        run: |
          cd backend
          python -m app.services.storage_cleanup cleanup-all
          python -m app.services.storage_cleanup cleanup-anonymous
```

#### Option C: Supabase pg_cron (Database-level)

Run in Supabase SQL Editor:

```sql
-- Enable pg_cron extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule daily cleanup at 2 AM UTC
SELECT cron.schedule(
  'daily-storage-cleanup',
  '0 2 * * *',
  $$
  -- Clean up old documents based on user subscription tiers
  DELETE FROM documents 
  WHERE id IN (
    SELECT d.id 
    FROM documents d
    JOIN subscriptions s ON d.user_id = s.user_id
    WHERE 
      -- Free tier: 1 day
      (s.tier = 'free' AND d.created_at < NOW() - INTERVAL '1 day')
      -- Basic tier: 7 days
      OR (s.tier = 'basic' AND d.created_at < NOW() - INTERVAL '7 days')
      -- Pro tier: 30 days
      OR (s.tier = 'pro' AND d.created_at < NOW() - INTERVAL '30 days')
      -- Ultra tier: 60 days
      OR (s.tier = 'ultra' AND d.created_at < NOW() - INTERVAL '60 days')
      -- Max tier: 90 days
      OR (s.tier = 'max' AND d.created_at < NOW() - INTERVAL '90 days')
  );
  
  -- Clean up anonymous uploads older than 24 hours
  DELETE FROM documents
  WHERE user_id IS NULL
  AND created_at < NOW() - INTERVAL '24 hours';
  $$
);

-- View scheduled jobs
SELECT * FROM cron.job;

-- Unschedule (if needed)
-- SELECT cron.unschedule('daily-storage-cleanup');
```

#### Option D: External Cron Service (EasyCron, cron-job.org)

1. Sign up for free account at https://cron-job.org
2. Create new cron job:
   - **URL**: `https://your-api.onrender.com/api/storage/cleanup/all`
   - **Method**: POST
   - **Schedule**: Daily at 2:00 AM
3. Add another for anonymous cleanup:
   - **URL**: `https://your-api.onrender.com/api/storage/cleanup/anonymous`
   - **Method**: POST
   - **Schedule**: Every 6 hours

## Monitoring Cleanup Operations

### Check Cleanup Logs

```python
# Add to your monitoring/logging system
import logging

logger = logging.getLogger(__name__)

# Logs are automatically generated:
# - "Cleaning up data for user {user_id} (tier: {tier}, retention: {days} days)"
# - "✅ Cleanup complete: X documents, Y invoices deleted"
```

### Set Up Alerts

#### Option 1: Sentry (Recommended)

```python
# In storage_cleanup.py
import sentry_sdk

try:
    result = cleanup_all_storage()
    if result.get('errors'):
        sentry_sdk.capture_message(f"Cleanup had errors: {result['errors']}", level="warning")
except Exception as e:
    sentry_sdk.capture_exception(e)
```

#### Option 2: Email Notifications

```python
# Add to storage_cleanup.py
from app.services.email_service import send_admin_email

result = cleanup_all_storage()
send_admin_email(
    subject="Daily Storage Cleanup Report",
    body=f"""
    Cleanup completed:
    - Users processed: {result['users_cleaned']}
    - Documents deleted: {result['total_documents_deleted']}
    - Invoices deleted: {result['total_invoices_deleted']}
    """
)
```

## Testing Cleanup

### 1. Test with Sample Data

```python
# Create test documents
from datetime import datetime, timedelta
from app.services.supabase_helper import supabase

# Create old document (should be deleted)
old_doc = {
    "user_id": "test-user-id",
    "created_at": (datetime.utcnow() - timedelta(days=10)).isoformat(),
    "file_url": "test-old.pdf"
}
supabase.table("documents").insert(old_doc).execute()

# Create recent document (should be kept)
new_doc = {
    "user_id": "test-user-id",
    "created_at": datetime.utcnow().isoformat(),
    "file_url": "test-new.pdf"
}
supabase.table("documents").insert(new_doc).execute()

# Run cleanup
python -m app.services.storage_cleanup cleanup-all

# Verify old deleted, new kept
```

### 2. Dry Run Mode

Add to `storage_cleanup.py`:

```python
def cleanup_user_data(user_id: str, tier: str, dry_run: bool = False):
    # ... existing code ...
    
    if dry_run:
        logger.info(f"DRY RUN: Would delete {len(document_ids)} documents")
        return {"would_delete": len(document_ids), "dry_run": True}
    
    # ... actual deletion code ...
```

## Production Checklist

- [ ] **Environment Variables**: Set SUPABASE_URL and SUPABASE_SERVICE_KEY
- [ ] **Choose Cleanup Method**: Select from options above
- [ ] **Schedule Job**: Set to run daily at low-traffic hours (2-4 AM)
- [ ] **Test First**: Run manual cleanup to verify it works
- [ ] **Monitor Logs**: Check cleanup logs after first run
- [ ] **Set Up Alerts**: Get notified of cleanup failures
- [ ] **Verify Storage Costs**: Confirm storage is decreasing
- [ ] **User Notification**: Warn users before data deletion (optional)

## User Notifications (Optional)

Warn users before their data is deleted:

```python
# Add to storage_cleanup.py
def notify_users_before_cleanup():
    """Send emails to users 3 days before data deletion"""
    # Get users with data expiring in 3 days
    # Send warning email
    # Let them upgrade to extend retention
```

## Troubleshooting

### Cleanup Not Running

1. Check cron job status
2. Verify environment variables
3. Check service logs
4. Test manual cleanup

### Data Not Being Deleted

1. Verify subscription tiers are correct
2. Check document created_at timestamps
3. Ensure foreign key constraints are correct
4. Run with logging enabled

### Performance Issues

1. Add database indexes:
```sql
CREATE INDEX idx_documents_user_created ON documents(user_id, created_at);
CREATE INDEX idx_documents_created ON documents(created_at);
```

2. Batch deletions (already implemented):
```python
# Delete in batches of 100
for i in range(0, len(document_ids), 100):
    batch = document_ids[i:i+100]
    # delete batch
```

## Cost Savings

Expected storage savings:

| Users | Avg Documents/User | Storage Saved/Month | Cost Savings |
|-------|-------------------|---------------------|--------------|
| 100 | 50 | ~5 GB | $0.50/month |
| 1,000 | 50 | ~50 GB | $5/month |
| 10,000 | 50 | ~500 GB | $50/month |

*Based on Supabase storage pricing: $0.10/GB/month*

## Support

If you need help:
1. Check logs: `python -m app.services.storage_cleanup cleanup-all`
2. Test manually: `python -m app.services.storage_cleanup stats <user_id>`
3. Review Supabase logs in dashboard
4. Contact support with error logs

---

**Last Updated**: October 23, 2025  
**Status**: ✅ Production Ready
