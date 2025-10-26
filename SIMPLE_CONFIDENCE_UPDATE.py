"""
Simple confidence score update using requests only (no supabase client)
"""
import requests
import json

def update_confidence_with_requests():
    """Update invoices using direct REST API calls"""
    
    SUPABASE_URL = "https://ldvwxqluaheuhbycdpwn.supabase.co"
    SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM"
    
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Fetching existing invoices...")
        
        # Get all invoices
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/invoices?select=id,vendor_name,total_amount,invoice_date,invoice_number",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch invoices: {response.status_code}")
            print(response.text)
            return
            
        invoices = response.json()
        print(f"📊 Found {len(invoices)} invoices to update")
        
        updated_count = 0
        
        for invoice in invoices:
            # Calculate confidence scores based on data quality
            confidence_score = 0.85
            vendor_confidence = 0.82
            amount_confidence = 0.88
            date_confidence = 0.85
            invoice_number_confidence = 0.80
            
            # Adjust based on actual data quality
            if invoice.get('vendor_name') and len(str(invoice['vendor_name'])) > 3:
                vendor_confidence = 0.90
                confidence_score += 0.05
            elif not invoice.get('vendor_name'):
                vendor_confidence = 0.65
                confidence_score -= 0.10
                
            if invoice.get('total_amount') and invoice['total_amount'] > 0:
                amount_confidence = 0.92
                confidence_score += 0.03
            else:
                amount_confidence = 0.60
                confidence_score -= 0.15
                
            if invoice.get('invoice_date'):
                date_confidence = 0.88
            else:
                date_confidence = 0.60
                confidence_score -= 0.10
                
            if invoice.get('invoice_number') and len(str(invoice['invoice_number'])) > 2:
                invoice_number_confidence = 0.85
            else:
                invoice_number_confidence = 0.55
                confidence_score -= 0.08
            
            # Ensure confidence score is within valid range
            confidence_score = max(0.50, min(0.98, confidence_score))
            
            # Update the invoice
            update_data = {
                'confidence_score': round(confidence_score, 2),
                'vendor_confidence': round(vendor_confidence, 2),
                'amount_confidence': round(amount_confidence, 2),
                'date_confidence': round(date_confidence, 2),
                'invoice_number_confidence': round(invoice_number_confidence, 2)
            }
            
            # PATCH request to update the invoice
            update_response = requests.patch(
                f"{SUPABASE_URL}/rest/v1/invoices?id=eq.{invoice['id']}",
                headers=headers,
                json=update_data
            )
            
            if update_response.status_code in [200, 204]:
                updated_count += 1
                print(f"✅ Updated invoice {invoice['id']} - Confidence: {confidence_score:.2f}")
            else:
                print(f"❌ Failed to update invoice {invoice['id']}: {update_response.status_code}")
        
        print(f"\n🎉 Successfully updated {updated_count}/{len(invoices)} invoices!")
        
        # Verify by fetching a few samples
        print("\n📊 Verifying updates...")
        verify_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/invoices?select=id,vendor_name,confidence_score,vendor_confidence&limit=5",
            headers=headers
        )
        
        if verify_response.status_code == 200:
            sample_invoices = verify_response.json()
            print("Sample updated invoices:")
            for inv in sample_invoices:
                print(f"ID: {inv['id']}, Vendor: {inv.get('vendor_name', 'N/A')}, "
                      f"Overall: {inv.get('confidence_score', 'N/A')}, "
                      f"Vendor: {inv.get('vendor_confidence', 'N/A')}")
        else:
            print(f"❌ Verification failed: {verify_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_confidence_with_requests()