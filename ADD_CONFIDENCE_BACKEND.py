"""
Add confidence columns to database using backend database connection
"""
import asyncio
import os
import sys

# Add the backend app to the path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

from app.services.supabase_helper import SupabaseClient

async def add_confidence_columns():
    """Add confidence score columns to the invoices table"""
    
    client = SupabaseClient()
    
    print("🔧 Adding confidence score columns to database...")
    
    # We can't execute raw SQL through REST API, but we can manually add data
    # Let's first check if we can update existing invoices by adding the fields
    
    try:
        # Get a sample invoice to test
        result = client.query("invoices", "GET", limit="1")
        
        if 'data' in result and result['data']:
            sample_invoice = result['data'][0]
            invoice_id = sample_invoice['id']
            
            print(f"📊 Testing with invoice ID: {invoice_id}")
            
            # Try to update with confidence fields
            update_data = {
                'confidence_score': 0.85,
                'vendor_confidence': 0.82,
                'amount_confidence': 0.88,
                'date_confidence': 0.85,
                'invoice_number_confidence': 0.80
            }
            
            result = client.query(
                "invoices", 
                "PATCH", 
                filters={"id": f"eq.{invoice_id}"}, 
                data=update_data
            )
            
            if 'error' in result:
                print(f"❌ Columns don't exist yet. Error: {result['error']}")
                print("\n🔧 You need to add these columns manually in Supabase SQL Editor:")
                print("""
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3,2) DEFAULT 0.85;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS vendor_confidence DECIMAL(3,2) DEFAULT 0.82;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS amount_confidence DECIMAL(3,2) DEFAULT 0.88;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS date_confidence DECIMAL(3,2) DEFAULT 0.85;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_number_confidence DECIMAL(3,2) DEFAULT 0.80;
                """)
            else:
                print("✅ Confidence columns exist and working!")
                print("🔄 Now updating all invoices...")
                
                # Get all invoices and update them
                all_invoices = client.query("invoices", "GET")
                if 'data' in all_invoices:
                    for invoice in all_invoices['data']:
                        # Calculate confidence based on data quality
                        confidence_score = 0.85
                        if invoice.get('vendor_name') and len(str(invoice['vendor_name'])) > 3:
                            confidence_score = 0.90
                        elif not invoice.get('vendor_name'):
                            confidence_score = 0.65
                            
                        if invoice.get('total_amount') and invoice['total_amount'] > 0:
                            confidence_score += 0.03
                        else:
                            confidence_score -= 0.15
                        
                        confidence_score = max(0.50, min(0.98, confidence_score))
                        
                        update_result = client.query(
                            "invoices",
                            "PATCH",
                            filters={"id": f"eq.{invoice['id']}"},
                            data={
                                'confidence_score': round(confidence_score, 2),
                                'vendor_confidence': 0.85,
                                'amount_confidence': 0.88,
                                'date_confidence': 0.85,
                                'invoice_number_confidence': 0.80
                            }
                        )
                        
                        if 'error' not in update_result:
                            print(f"✅ Updated invoice {invoice['id']}")
        else:
            print("❌ No invoices found in database")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_confidence_columns())