"""
Execute WEBHOOK_LOGS_MIGRATION.sql in Supabase
Creates webhook_logs table with indexes and triggers
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

try:
    from app.config.database import supabase
except ImportError:
    # If import fails, we'll provide manual instructions
    supabase = None

def run_migration():
    """Execute webhook logs migration SQL"""
    
    print("=" * 70)
    print("🔄 EXECUTING WEBHOOK LOGS MIGRATION")
    print("=" * 70)
    
    # Read SQL file
    sql_file = Path(__file__).parent.parent.parent / "WEBHOOK_LOGS_MIGRATION.sql"
    
    if not sql_file.exists():
        print(f"❌ SQL file not found: {sql_file}")
        return False
    
    print(f"📄 Reading SQL from: {sql_file.name}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print(f"📝 SQL size: {len(sql)} characters")
    
    try:
        # Execute SQL via Supabase
        print("\n🚀 Executing SQL in Supabase...")
        
        # Use the REST API to execute SQL
        response = supabase.rpc('exec_sql', {'query': sql}).execute()
        
        print("✅ Migration executed successfully!")
        print("\n📊 Verifying webhook_logs table...")
        
        # Verify table exists
        result = supabase.table('webhook_logs').select('count', count='exact').limit(0).execute()
        
        print(f"✅ webhook_logs table exists (count: {result.count})")
        print("\n" + "=" * 70)
        print("✅ WEBHOOK LOGS MIGRATION COMPLETE")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        
        # If exec_sql RPC doesn't exist, provide manual instructions
        if 'exec_sql' in error_msg.lower() or 'function' in error_msg.lower():
            print("\n⚠️  Note: Direct SQL execution via Python requires custom RPC function")
            print("\n📋 MANUAL MIGRATION INSTRUCTIONS:")
            print("=" * 70)
            print("1. Open Supabase SQL Editor:")
            print("   https://supabase.com/dashboard/project/ldvwxqluaheuhbycdpwn/sql")
            print("\n2. Copy the contents of WEBHOOK_LOGS_MIGRATION.sql")
            print("\n3. Paste and run in the SQL editor")
            print("\n4. Verify with this query:")
            print("   SELECT COUNT(*) FROM webhook_logs;")
            print("=" * 70)
            
            return "manual"
        else:
            print(f"\n❌ Migration failed: {error_msg}")
            return False

if __name__ == "__main__":
    result = run_migration()
    
    if result == "manual":
        print("\n⏸️  Manual migration required - see instructions above")
        sys.exit(2)
    elif result:
        print("\n✅ All done! Webhook logs table is ready.")
        sys.exit(0)
    else:
        print("\n❌ Migration failed")
        sys.exit(1)
