"""
Test confidence scores are working properly
"""
import requests
import json

def test_confidence_scores():
    """Test that confidence scores are now available in the database"""
    
    SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
    SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM"
    
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Testing confidence scores in database...")
        
        # Fetch invoices with confidence scores
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/invoices?select=id,vendor_name,total_amount,confidence_score,vendor_confidence,amount_confidence&limit=5",
            headers=headers
        )
        
        if response.status_code == 200:
            invoices = response.json()
            print(f"✅ Successfully fetched {len(invoices)} invoices with confidence scores!")
            
            print("\n📊 Sample invoices with confidence data:")
            for invoice in invoices:
                print(f"""
Invoice ID: {invoice.get('id', 'N/A')}
Vendor: {invoice.get('vendor_name', 'N/A')}
Amount: {invoice.get('total_amount', 'N/A')}
Overall Confidence: {invoice.get('confidence_score', 'N/A')}
Vendor Confidence: {invoice.get('vendor_confidence', 'N/A')}
Amount Confidence: {invoice.get('amount_confidence', 'N/A')}
---""")
            
            # Check if any invoices have confidence scores
            has_confidence = any(invoice.get('confidence_score') for invoice in invoices)
            
            if has_confidence:
                print("🎉 SUCCESS! Confidence scores are working!")
                print("✅ Frontend should now display confidence indicators")
                print("🌟 Check your browser at http://localhost:3001/invoices")
            else:
                print("❌ No confidence scores found. SQL might not have executed properly.")
                
        else:
            print(f"❌ Failed to fetch invoices: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error testing confidence scores: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_confidence_scores()