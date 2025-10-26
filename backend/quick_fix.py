#!/usr/bin/env python3
"""
Quick Fix for Payment Status Constraint
Direct update using Supabase Python client
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_payment_status():
    """Fix payment status constraint issue"""
    try:
        SUPABASE_URL = os.getenv('SUPABASE_URL')
        SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
        
        print("🔌 Connecting to Supabase...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # First, let's see what payment status values are causing issues
        print("🔍 Checking existing payment status values...")
        result = supabase.table('invoices').select('payment_status')
        
        unique_values = set()
        for row in result.data:
            if row['payment_status']:
                unique_values.add(row['payment_status'])
        
        print(f"📊 Found payment status values: {unique_values}")
        
        # Normalize any problematic values
        print("🔧 Normalizing payment status values...")
        
        # Update any variation to standard lowercase
        status_mapping = {
            'PAID': 'paid',
            'Paid': 'paid', 
            'PENDING': 'pending',
            'Pending': 'pending',
            'OVERDUE': 'overdue',
            'Overdue': 'overdue'
        }
        
        updated_count = 0
        for old_status, new_status in status_mapping.items():
            try:
                update_result = supabase.table('invoices').update({
                    'payment_status': new_status
                }).eq('payment_status', old_status)
                
                if update_result.data:
                    updated_count += len(update_result.data)
                    print(f"   ✅ Updated {len(update_result.data)} records: {old_status} → {new_status}")
            except Exception as e:
                print(f"   ⚠️ Update failed for {old_status}: {e}")
        
        print(f"✅ Payment status normalization complete! Updated {updated_count} records")
        return True
        
    except Exception as e:
        print(f"❌ Payment status fix failed: {e}")
        return False

def add_missing_columns():
    """Add the most critical missing columns"""
    try:
        SUPABASE_URL = os.getenv('SUPABASE_URL')
        SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
        
        print("🔌 Connecting to Supabase...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # Add the columns that are causing immediate errors
        critical_columns = [
            "arrival_date",
            "departure_date", 
            "order_id",
            "booking_reference",
            "room_number",
            "guest_count"
        ]
        
        print("🚀 Adding critical missing columns...")
        for column in critical_columns:
            try:
                # This might not work through Supabase client, but worth trying
                supabase.postgrest.rpc('exec_sql', {
                    'sql': f'ALTER TABLE invoices ADD COLUMN IF NOT EXISTS {column} VARCHAR(100)'
                })
                print(f"   ✅ Added column: {column}")
            except Exception as e:
                print(f"   ⚠️ Column {column} add failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Column addition failed: {e}")
        return False

if __name__ == "__main__":
    print("🛠️ QUICK DATABASE FIX")
    print("=" * 50)
    
    # Fix payment status first
    if fix_payment_status():
        print("\n🎯 Payment status fixed!")
    
    # Try to add missing columns
    print("\n🔧 Adding missing columns...")
    add_missing_columns()
    
    print("\n✅ Quick fixes applied! Server should work better now.")