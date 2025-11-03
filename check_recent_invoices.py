"""
Check most recent invoices to see if upload worked
"""
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment from backend/.env
load_dotenv("backend/.env")

# Initialize Supabase with SERVICE_KEY (bypasses RLS)
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")

if not supabase_service_key:
    print("❌ SUPABASE_SERVICE_KEY not found in .env")
    exit(1)

supabase = create_client(supabase_url, supabase_service_key)

print("✅ Connected to Supabase with SERVICE_KEY (bypasses RLS)")
print("=" * 80)

# Get most recent 5 invoices
try:
    response = supabase.table("invoices").select(
        "id, invoice_number, vendor_name, customer_name, total_amount, created_at, user_id"
    ).order("created_at", desc=True).limit(5).execute()
    
    if response.data:
        print(f"📊 Found {len(response.data)} recent invoices:\n")
        
        for i, inv in enumerate(response.data, 1):
            print(f"{i}. Invoice #{inv.get('invoice_number', 'N/A')}")
            print(f"   ID: {inv['id']}")
            print(f"   Vendor: {inv.get('vendor_name', 'N/A')}")
            print(f"   Customer: {inv.get('customer_name', 'N/A')}")
            print(f"   Amount: ₹{inv.get('total_amount', 0)}")
            print(f"   User ID: {inv.get('user_id', 'N/A')}")
            print(f"   Created: {inv.get('created_at', 'N/A')}")
            
            # Check if this is the problem invoice
            if inv['id'] == '106f005b-1f17-40b1-8f0b-60ceb1bca773':
                print(f"   🎯 THIS IS THE INVOICE FROM THE ERROR!")
            print()
        
        # Check the specific invoice from the error
        problem_id = '106f005b-1f17-40b1-8f0b-60ceb1bca773'
        print("=" * 80)
        print(f"🔍 Checking specific invoice: {problem_id}")
        
        specific = supabase.table("invoices").select("*").eq("id", problem_id).execute()
        
        if specific.data:
            inv = specific.data[0]
            print(f"✅ Invoice EXISTS in database!")
            print(f"   Invoice #: {inv.get('invoice_number', 'N/A')}")
            print(f"   Vendor: {inv.get('vendor_name', 'N/A')}")
            print(f"   Vendor GSTIN: {inv.get('vendor_gstin', 'N/A')}")
            print(f"   Customer: {inv.get('customer_name', 'N/A')}")
            print(f"   Customer GSTIN: {inv.get('customer_gstin', 'N/A')}")
            print(f"   Total: ₹{inv.get('total_amount', 0)}")
            print(f"   User ID: {inv.get('user_id', 'N/A')}")
            print(f"\n🚨 PROBLEM: Frontend getting 401 because of RLS policy!")
            print(f"   Solution: Check RLS policies on 'invoices' table")
        else:
            print(f"❌ Invoice NOT found in database")
        
    else:
        print("❌ No invoices found in database")
        
except Exception as e:
    print(f"❌ Error: {e}")
