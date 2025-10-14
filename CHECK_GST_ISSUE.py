"""
Check GST Issue - Why Excel has GST when invoice doesn't
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def check_invoice_gst():
    """Check GST values in the invoice that was just uploaded"""
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Missing Supabase credentials")
        return
    
    print("🔍 CHECKING GST VALUES IN DATABASE...")
    print("=" * 60)
    
    # Get all invoices to find the Meenakshi Tour invoice
    url = f"{SUPABASE_URL}/rest/v1/invoices"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params={"select": "*"})
        
        if response.status_code == 200:
            invoices = response.json()
            
            # Find the Meenakshi Tour invoice
            target_invoice = None
            for inv in invoices:
                if inv.get('vendor_name') == 'MEENAKSHI TOUR & TRAVEL':
                    target_invoice = inv
                    break
            
            if target_invoice:
                print(f"✅ Found invoice: {target_invoice.get('invoice_number')}")
                print(f"   Vendor: {target_invoice.get('vendor_name')}")
                print(f"   Total Amount: ₹{target_invoice.get('total_amount', 0)}")
                print()
                print("💰 TAX VALUES IN DATABASE:")
                print(f"   Subtotal: ₹{target_invoice.get('subtotal') or 0}")
                print(f"   CGST: ₹{target_invoice.get('cgst') or 0}")
                print(f"   SGST: ₹{target_invoice.get('sgst') or 0}")
                print(f"   IGST: ₹{target_invoice.get('igst') or 0}")
                print()
                
                # Check if GST values are NULL or 0
                cgst = target_invoice.get('cgst')
                sgst = target_invoice.get('sgst')
                igst = target_invoice.get('igst')
                
                if cgst is None and sgst is None and igst is None:
                    print("✅ CORRECT: No GST values stored (all NULL)")
                    print("🔍 ISSUE: Export system must be calculating GST artificially")
                elif cgst == 0 and sgst == 0 and igst == 0:
                    print("✅ CORRECT: All GST values are 0")
                    print("🔍 ISSUE: Export system must be calculating GST artificially")
                else:
                    print("❌ PROBLEM: GST values are stored in database:")
                    print(f"   CGST: {cgst}")
                    print(f"   SGST: {sgst}")
                    print(f"   IGST: {igst}")
                    print("🔍 ISSUE: AI extractor incorrectly added GST to non-GST invoice")
                
                print()
                print("📋 RAW EXTRACTED DATA:")
                raw_data = target_invoice.get('raw_extracted_data')
                if raw_data:
                    import json
                    print(json.dumps(raw_data, indent=2))
                else:
                    print("   No raw data stored")
                    
            else:
                print("❌ MEENAKSHI TOUR & TRAVEL invoice not found")
                print("📋 Available invoices:")
                for inv in invoices:
                    print(f"   - {inv.get('vendor_name')} (₹{inv.get('total_amount', 0)})")
        else:
            print(f"❌ Failed to fetch invoices: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_invoice_gst()