"""
Check and add confidence score field to database
"""
import psycopg2
import os

def check_confidence_fields():
    try:
        # Connect to Supabase database
        conn = psycopg2.connect(
            "postgresql://postgres.ldvwxqluaheuhbycdpwn:3dnH9VLVlM7sc8i4@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
        )
        cur = conn.cursor()
        
        # Check if confidence_score column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'invoices' 
            AND column_name LIKE '%confidence%';
        """)
        
        confidence_cols = cur.fetchall()
        print("🔍 Existing confidence columns:", confidence_cols)
        
        if not confidence_cols:
            print("❌ No confidence_score column found!")
            print("🔧 Adding confidence_score column...")
            
            # Add confidence_score column
            cur.execute("""
                ALTER TABLE invoices 
                ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3,2) DEFAULT 0.0;
            """)
            
            # Add individual confidence fields for detailed tracking
            cur.execute("""
                ALTER TABLE invoices 
                ADD COLUMN IF NOT EXISTS vendor_confidence DECIMAL(3,2) DEFAULT 0.0,
                ADD COLUMN IF NOT EXISTS amount_confidence DECIMAL(3,2) DEFAULT 0.0,
                ADD COLUMN IF NOT EXISTS date_confidence DECIMAL(3,2) DEFAULT 0.0,
                ADD COLUMN IF NOT EXISTS invoice_number_confidence DECIMAL(3,2) DEFAULT 0.0;
            """)
            
            conn.commit()
            print("✅ Confidence columns added successfully!")
        else:
            print("✅ Confidence columns already exist")
            
        # Check current invoice data
        cur.execute("""
            SELECT id, vendor_name, confidence_score, vendor_confidence 
            FROM invoices 
            LIMIT 5;
        """)
        
        sample_data = cur.fetchall()
        print("\n📊 Sample invoice data with confidence scores:")
        for row in sample_data:
            print(f"ID: {row[0]}, Vendor: {row[1]}, Overall: {row[2]}, Vendor: {row[3]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_confidence_fields()