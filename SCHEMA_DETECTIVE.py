#!/usr/bin/env python3
"""
SCHEMA DETECTIVE: Find out which payment_status constraint is ACTUALLY active in database
"""

import asyncio
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") 
supabase: Client = create_client(url, key)

async def check_database_constraint():
    """Check the actual payment_status constraint in the database"""
    
    print("🔍 TESTING ACTUAL DATABASE PAYMENT_STATUS CONSTRAINT...")
    print()
    
    # Test each possible payment_status value to see which ones are accepted
    test_values = ['paid', 'unpaid', 'partial', 'overdue', 'pending', 'cancelled', 'refunded', 'invalid_test']
    
    results = {}
    
    for test_value in test_values:
        try:
            # Create a test invoice record
            test_data = {
                'user_id': 'd1949c37-d380-46f4-ad30-20ae84aff1ad',  # Known user ID
                'document_id': '825b1b43-bc59-4204-8e91-e75cb721966f',  # Known document ID  
                'filename': f'test_{test_value}',
                'vendor_name': 'Test Vendor',  # NOT NULL requirement
                'payment_status': test_value,
                'total_amount': 100.00,
                'currency': 'INR'
            }
            
            print(f"Testing payment_status = '{test_value}'...")
            
            # Try to insert - this will reveal the actual constraint
            result = supabase.table('invoices').insert(test_data).execute()
            
            if result.data:
                print(f"✅ ACCEPTED: '{test_value}'")
                results[test_value] = "ACCEPTED"
                # Clean up - delete the test record
                supabase.table('invoices').delete().eq('id', result.data[0]['id']).execute()
            else:
                print(f"❌ REJECTED: '{test_value}'")
                results[test_value] = "REJECTED"
                
        except Exception as e:
            error_msg = str(e)
            if "23514" in error_msg and "payment_status_check" in error_msg:
                print(f"❌ CONSTRAINT VIOLATION: '{test_value}' - {error_msg[:100]}...")
                results[test_value] = "CONSTRAINT_VIOLATION"
            else:
                print(f"⚠️  OTHER ERROR: '{test_value}' - {error_msg[:100]}...")
                results[test_value] = f"ERROR: {error_msg[:50]}"
    
    print()
    print("🎯 ACTUAL DATABASE CONSTRAINT RESULTS:")
    print("=" * 50)
    
    accepted = [k for k, v in results.items() if v == "ACCEPTED"]
    rejected = [k for k, v in results.items() if "CONSTRAINT_VIOLATION" in v or v == "REJECTED"]
    
    print(f"✅ ACCEPTED VALUES: {accepted}")
    print(f"❌ REJECTED VALUES: {rejected}")
    print()
    
    if 'unpaid' in rejected:
        print("🚨 CRITICAL DISCOVERY: 'unpaid' is REJECTED by database!")
        print("    This explains why our fixes aren't working!")
    
    if accepted:
        print(f"💡 RECOMMENDATION: Use one of the accepted values as default: {accepted[0]}")
    
    print()
    print("🔍 Now we know the EXACT constraint the database is using!")

if __name__ == "__main__":
    asyncio.run(check_database_constraint())