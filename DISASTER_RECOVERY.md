# 🆘 DISASTER RECOVERY PLAN

**Last Updated:** October 26, 2025  
**Owner:** TrulyInvoice DevOps Team  
**Review Frequency:** Quarterly

---

## 📋 TABLE OF CONTENTS

1. [Recovery Objectives](#recovery-objectives)
2. [Backup Schedule](#backup-schedule)
3. [Emergency Contacts](#emergency-contacts)
4. [Recovery Procedures](#recovery-procedures)
5. [Testing Schedule](#testing-schedule)
6. [Incident Response](#incident-response)

---

## 🎯 RECOVERY OBJECTIVES

### RTO (Recovery Time Objective)
**Target: 4 hours**  
Maximum acceptable time to restore services after an incident.

### RPO (Recovery Point Objective)
**Target: 24 hours**  
Maximum acceptable data loss measured in time.

### Service Level Agreement (SLA)
- **Uptime Target:** 99.5% (43.8 hours downtime/year)
- **Response Time:** Critical incidents < 1 hour
- **Resolution Time:** Critical incidents < 4 hours

---

## 💾 BACKUP SCHEDULE

### Database Backups (Supabase)
- **Frequency:** Daily at 2:00 AM UTC
- **Retention:** 7 days (free tier), 30 days (Pro tier)
- **Type:** Full database snapshot
- **Location:** Supabase managed backups
- **Automatic:** Yes ✅
- **Access:** https://app.supabase.com/project/_/database/backups

### File Storage Backups (Supabase Storage)
- **Frequency:** Continuous (versioning enabled)
- **Retention:** Latest 100 versions per file
- **Type:** Incremental
- **Location:** Supabase Storage with versioning
- **Automatic:** Yes ✅
- **Access:** https://app.supabase.com/project/_/storage/buckets

### Code Repository (GitHub)
- **Frequency:** Every commit
- **Retention:** Unlimited
- **Type:** Git version control
- **Location:** GitHub.com
- **Automatic:** Yes ✅
- **Access:** https://github.com/your-org/trulyinvoice.xyz

### Configuration Backups
- **Frequency:** Manual on changes
- **Retention:** Git history
- **Files to backup:**
  - `.env.example` (never commit actual `.env`)
  - `vercel.json`
  - `render.yaml`
  - All SQL migration files
  - Documentation files

---

## 📞 EMERGENCY CONTACTS

### Primary Contacts
| Role | Name | Phone | Email | Availability |
|------|------|-------|-------|--------------|
| System Admin | [Your Name] | [Phone] | [Email] | 24/7 |
| Backend Lead | [Name] | [Phone] | [Email] | Business hours |
| Frontend Lead | [Name] | [Phone] | [Email] | Business hours |

### Service Providers
| Service | Support URL | Emergency Contact |
|---------|-------------|-------------------|
| Supabase | https://supabase.com/support | support@supabase.io |
| Vercel | https://vercel.com/support | support@vercel.com |
| Render | https://render.com/support | support@render.com |
| Sentry | https://sentry.io/support | support@sentry.io |
| Domain Registrar | [Your registrar] | [Contact] |

### Escalation Path
1. **Level 1:** On-call engineer (response: 15 min)
2. **Level 2:** System admin (response: 30 min)
3. **Level 3:** External support (response: 1-4 hours)

---

## 🔧 RECOVERY PROCEDURES

### 1. DATABASE RESTORATION

#### **Scenario:** Database corruption or data loss

#### **Steps:**

1. **Assess the Damage**
   ```bash
   # Check database status
   curl https://your-project.supabase.co/rest/v1/
   
   # Check table counts
   SELECT 
     'invoices' as table_name, COUNT(*) as count FROM invoices
   UNION ALL
   SELECT 'documents', COUNT(*) FROM documents
   UNION ALL
   SELECT 'users', COUNT(*) FROM users;
   ```

2. **Access Supabase Dashboard**
   - Go to: https://app.supabase.com/project/_/database/backups
   - Log in with admin credentials

3. **Select Backup**
   - Review available backups (last 7-30 days)
   - Choose backup from before incident
   - Note: backup timestamp and size

4. **Restore Backup**
   ```
   Option A: Point-in-Time Recovery (Pro plan only)
   - Click "Point in Time Recovery"
   - Select exact timestamp
   - Click "Restore"
   - Estimated time: 10-15 minutes
   
   Option B: Full Backup Restore (All plans)
   - Click on desired backup
   - Click "Restore this backup"
   - Confirm restoration
   - Estimated time: 15-30 minutes
   ```

5. **Verify Restoration**
   ```sql
   -- Check data integrity
   SELECT COUNT(*) FROM invoices WHERE created_at >= '2025-10-01';
   SELECT COUNT(*) FROM documents WHERE uploaded_at >= '2025-10-01';
   SELECT COUNT(*) FROM users WHERE created_at >= '2025-10-01';
   
   -- Check recent records
   SELECT * FROM invoices ORDER BY created_at DESC LIMIT 10;
   ```

6. **Test Application**
   ```bash
   # Test API health
   curl https://api.trulyinvoice.xyz/health
   
   # Test authentication
   curl -X POST https://api.trulyinvoice.xyz/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test"}'
   
   # Test invoice retrieval
   curl https://api.trulyinvoice.xyz/api/invoices \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

7. **Notify Users** (if data loss occurred)
   - Send email to affected users
   - Post status update
   - Document incident

**Estimated Recovery Time:** 30-45 minutes

---

### 2. FILE STORAGE RESTORATION

#### **Scenario:** Uploaded files deleted or corrupted

#### **Steps:**

1. **Identify Missing Files**
   ```sql
   -- Find documents without files
   SELECT id, file_name, uploaded_at 
   FROM documents 
   WHERE file_path IS NULL OR file_path = '';
   ```

2. **Access Supabase Storage**
   - Go to: https://app.supabase.com/project/_/storage/buckets
   - Select bucket: `invoices` or `documents`

3. **Restore File Versions**
   ```
   - Navigate to file location
   - Click file name
   - Click "History" tab
   - Select version before deletion
   - Click "Restore this version"
   ```

4. **Bulk Restoration** (if many files)
   ```javascript
   // Use Supabase Storage API
   const { data, error } = await supabase
     .storage
     .from('invoices')
     .list('folder-path', {
       limit: 100,
       offset: 0,
     })
   ```

5. **Verify Files**
   ```bash
   # Test file access
   curl https://your-project.supabase.co/storage/v1/object/public/invoices/test.pdf
   ```

**Estimated Recovery Time:** 15-30 minutes

---

### 3. APPLICATION ROLLBACK

#### **Scenario:** Bad deployment breaks application

#### **Steps:**

1. **Identify Last Working Version**
   ```bash
   # View recent commits
   git log --oneline -10
   
   # Check deployment history
   # Vercel: https://vercel.com/dashboard/deployments
   # Render: https://dashboard.render.com
   ```

2. **Rollback Backend (Render)**
   ```bash
   # Option A: Redeploy previous version via dashboard
   # - Go to Render dashboard
   # - Select service
   # - Click "Manual Deploy"
   # - Select previous commit
   
   # Option B: Git rollback
   git revert HEAD
   git push origin main
   # Render auto-deploys from main branch
   ```

3. **Rollback Frontend (Vercel)**
   ```bash
   # Option A: Instant rollback via dashboard
   # - Go to Vercel deployments
   # - Find last working deployment
   # - Click "..." > "Promote to Production"
   
   # Option B: Git rollback
   cd frontend
   git revert HEAD
   git push origin main
   # Vercel auto-deploys from main branch
   ```

4. **Verify Rollback**
   ```bash
   # Check API version
   curl https://api.trulyinvoice.xyz/ | jq '.version'
   
   # Check frontend
   curl -I https://trulyinvoice.xyz
   
   # Test critical paths
   # - Login
   # - Upload invoice
   # - View invoices
   # - Export data
   ```

5. **Monitor for Issues**
   ```bash
   # Check Sentry for errors
   # https://sentry.io/organizations/your-org/issues/
   
   # Check server logs
   # Render: https://dashboard.render.com/logs
   ```

**Estimated Recovery Time:** 10-20 minutes

---

### 4. DNS/DOMAIN RECOVERY

#### **Scenario:** Domain not resolving or DNS issues

#### **Steps:**

1. **Verify DNS Status**
   ```bash
   # Check DNS resolution
   nslookup trulyinvoice.xyz
   dig trulyinvoice.xyz
   
   # Check DNS propagation
   # Use: https://www.whatsmydns.net/#A/trulyinvoice.xyz
   ```

2. **Check DNS Records**
   ```
   Current DNS Configuration:
   
   A Record:
   - Name: @
   - Value: 76.76.21.21 (Vercel)
   - TTL: 300
   
   CNAME Record:
   - Name: www
   - Value: cname.vercel-dns.com
   - TTL: 300
   
   CNAME Record (API):
   - Name: api
   - Value: trulyinvoice-backend.onrender.com
   - TTL: 300
   ```

3. **Access Domain Registrar**
   - Provider: [Your domain registrar]
   - Login: [Dashboard URL]
   - Navigate to DNS settings

4. **Restore DNS Records**
   ```
   If records are missing or incorrect:
   
   1. Delete incorrect records
   2. Add correct records (see above)
   3. Save changes
   4. Wait for propagation (5-30 minutes)
   ```

5. **Verify Resolution**
   ```bash
   # Test after 5 minutes
   curl -I https://trulyinvoice.xyz
   curl -I https://api.trulyinvoice.xyz
   
   # Check SSL certificate
   openssl s_client -connect trulyinvoice.xyz:443 -servername trulyinvoice.xyz
   ```

**Estimated Recovery Time:** 5-30 minutes (due to DNS propagation)

---

### 5. COMPLETE SERVICE OUTAGE

#### **Scenario:** All services down

#### **Steps:**

1. **Triage** (First 5 minutes)
   ```
   Check Status Pages:
   - Supabase: https://status.supabase.com
   - Vercel: https://www.vercel-status.com
   - Render: https://status.render.com
   
   Quick Tests:
   - ping trulyinvoice.xyz
   - curl https://api.trulyinvoice.xyz/health
   - curl https://trulyinvoice.xyz
   ```

2. **Identify Root Cause** (5-15 minutes)
   ```
   Common causes:
   □ Service provider outage
   □ DNS issues
   □ SSL certificate expired
   □ Database connection failure
   □ API rate limit exceeded
   □ Bad deployment
   □ DDoS attack
   ```

3. **Emergency Response** (15-30 minutes)
   ```
   If provider outage:
   - Wait for provider resolution
   - Monitor status pages
   - Notify users via social media
   
   If our issue:
   - Follow relevant recovery procedure above
   - Check Sentry for errors
   - Review recent deployments
   - Check database connections
   ```

4. **Communicate** (Throughout)
   ```
   - Update status page (if available)
   - Tweet from company account
   - Email affected users
   - Update incident log
   ```

5. **Post-Incident Review** (After resolution)
   ```
   - Document what happened
   - Update runbook
   - Implement preventive measures
   - Schedule team retrospective
   ```

**Estimated Recovery Time:** 30 minutes - 4 hours

---

## 🧪 TESTING SCHEDULE

### Quarterly Tests (Every 3 Months)
- [ ] Test database restoration
- [ ] Test file storage restoration
- [ ] Test application rollback
- [ ] Verify all backup systems running
- [ ] Update contact information
- [ ] Review and update procedures

### Annual Tests (Once per Year)
- [ ] Full disaster recovery simulation
- [ ] Test complete system rebuild
- [ ] Verify insurance coverage
- [ ] Update disaster recovery plan
- [ ] Train new team members

### After Major Changes
- [ ] Test backups after schema changes
- [ ] Test restoration after infrastructure changes
- [ ] Update documentation

---

## 📊 INCIDENT RESPONSE PROCEDURE

### Severity Levels

#### **P0 - Critical (Drop Everything)**
- Complete service outage
- Data breach
- Payment system down
- **Response Time:** 15 minutes
- **Resolution Target:** 4 hours

#### **P1 - High (Fix Today)**
- Partial service outage
- Major feature broken
- Performance degradation >50%
- **Response Time:** 1 hour
- **Resolution Target:** 24 hours

#### **P2 - Medium (Fix This Week)**
- Minor feature broken
- Performance degradation <50%
- Non-critical errors
- **Response Time:** 4 hours
- **Resolution Target:** 1 week

#### **P3 - Low (Fix Next Sprint)**
- UI bugs
- Enhancement requests
- Documentation updates
- **Response Time:** 1 day
- **Resolution Target:** 2 weeks

### Response Steps

1. **ACKNOWLEDGE** (Immediate)
   - Acknowledge incident in monitoring tool
   - Notify team via Slack/Discord
   - Set severity level

2. **ASSESS** (First 15 minutes)
   - Gather information
   - Identify affected services
   - Estimate impact (users, revenue)
   - Determine root cause

3. **RESPOND** (15-60 minutes)
   - Follow relevant recovery procedure
   - Keep stakeholders updated
   - Document actions taken

4. **RESOLVE** (Target: 4 hours)
   - Fix root cause
   - Verify resolution
   - Monitor for recurrence

5. **REVIEW** (Within 48 hours)
   - Write post-mortem
   - Share learnings
   - Implement preventive measures
   - Update runbooks

---

## 📝 INCIDENT LOG

### Template

```markdown
## Incident: [Brief Description]

**Date:** YYYY-MM-DD  
**Time Started:** HH:MM UTC  
**Time Resolved:** HH:MM UTC  
**Duration:** X hours  
**Severity:** P0/P1/P2/P3  
**Affected Users:** X users  

### What Happened
[Description]

### Root Cause
[Technical details]

### Resolution
[What was done to fix it]

### Preventive Measures
- [ ] Action item 1
- [ ] Action item 2

### Lessons Learned
[Key takeaways]
```

### Recent Incidents
_(Document all incidents here)_

---

## 🔐 ACCESS CREDENTIALS

### Where to Find Credentials

**NEVER store actual credentials in this document!**

Credentials are stored securely in:
- **1Password** (Team vault)
- **Environment variables** (.env files on servers)
- **Vercel Dashboard** (Environment variables)
- **Render Dashboard** (Environment variables)
- **Supabase Dashboard** (API keys section)

### Emergency Access
If primary admin is unavailable:
1. Access shared password manager (1Password)
2. Use "Emergency Access" feature
3. Contact service providers for account recovery

---

## 📚 ADDITIONAL RESOURCES

### Documentation
- [Deployment Guide](DEPLOYMENT_GUIDE_FINAL.md)
- [Architecture Overview](ARCHITECTURE.md)
- [API Documentation](/docs)
- [Database Schema](SUPABASE_SCHEMA.sql)

### External Resources
- [Supabase Backup Documentation](https://supabase.com/docs/guides/platform/backups)
- [Vercel Rollback Guide](https://vercel.com/docs/deployments/rollbacks)
- [Render Rollback Guide](https://render.com/docs/deploys#rolling-back-a-deploy)
- [PostgreSQL Backup Best Practices](https://www.postgresql.org/docs/current/backup.html)

### Monitoring Tools
- **Uptime:** UptimeRobot.com
- **Errors:** Sentry.io
- **Performance:** Vercel Analytics
- **Logs:** Render Dashboard

---

## ✅ PRE-INCIDENT CHECKLIST

Complete this checklist to ensure readiness:

- [ ] All team members have access to this document
- [ ] Emergency contacts are up to date
- [ ] Backup systems verified working
- [ ] Access credentials documented (in password manager)
- [ ] Testing schedule followed
- [ ] Monitoring alerts configured
- [ ] Incident response roles assigned
- [ ] Communication channels established
- [ ] Quarterly DR test completed
- [ ] Post-mortem template ready

---

## 📅 REVIEW LOG

| Date | Reviewer | Changes Made | Next Review |
|------|----------|--------------|-------------|
| 2025-10-26 | System | Initial creation | 2026-01-26 |
| | | | |

---

**END OF DISASTER RECOVERY PLAN**

*This is a living document. Update it whenever procedures change, contacts change, or after any incident.*
