"""
Update existing invoices with confidence scores using Supabase Python client
"""
from supabase import create_client, Client
import os

def update_invoice_confidence_scores():
    """Update all existing invoices with realistic confidence scores"""
    
    # Initialize Supabase client
    url = "https://ldvwxqluaheuhbycdpwn.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdnd4cWx1YWhldWhieWNkcHduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDA3NjY1NiwiZXhwIjoyMDc1NjUyNjU2fQ.939ySYuwA9ByCprCiI9GL5xEmvkhONYEWdtuHVLweWM"
    
    supabase: Client = create_client(url, key)
    
    try:
        print("🔄 Updating existing invoices with confidence scores...")
        
        # Fetch all invoices
        response = supabase.table("invoices").select("*").execute()
        invoices = response.data
        
        print(f"📊 Found {len(invoices)} invoices to update")
        
        updated_count = 0
        for invoice in invoices:
            # Calculate confidence scores based on data quality
            confidence_score = 0.85  # Default
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
            elif not invoice.get('total_amount'):
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
            
            result = supabase.table("invoices").update(update_data).eq('id', invoice['id']).execute()
            
            if result.data:
                updated_count += 1
                print(f"✅ Updated invoice {invoice['id']} - Confidence: {confidence_score:.2f}")
            else:
                print(f"❌ Failed to update invoice {invoice['id']}")
        
        print(f"\n🎉 Successfully updated {updated_count}/{len(invoices)} invoices with confidence scores!")
        
        # Verify updates by fetching a sample
        sample = supabase.table("invoices").select("id,vendor_name,confidence_score,vendor_confidence").limit(5).execute()
        
        print("\n📊 Sample updated invoices:")
        for inv in sample.data:
            print(f"ID: {inv['id']}, Vendor: {inv['vendor_name']}, Overall: {inv['confidence_score']}, Vendor: {inv['vendor_confidence']}")
            
    except Exception as e:
        print(f"❌ Error updating confidence scores: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_invoice_confidence_scores()