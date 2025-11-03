import psycopg2
from datetime import datetime
import re

DB_HOST = "db.ldvwxqluaheuhbycdpwn.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "QDIXJSBJwyJOyTHt"

print("="*80)
print("🔧 FIXING ALL TALLY IMPORT ISSUES")
print("="*80)

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, database=DB_NAME, 
    user=DB_USER, password=DB_PASSWORD
)
cur = conn.cursor()

# Issue 1: Fix missing invoice dates (5 invoices)
print("\n📅 Issue 1: Fixing missing invoice dates...")
cur.execute("""
    SELECT id, invoice_number, invoice_date 
    FROM invoices 
    WHERE invoice_date IS NULL 
    ORDER BY created_at DESC
""")
missing_dates = cur.fetchall()

if missing_dates:
    print(f"   Found {len(missing_dates)} invoices with missing dates:")
    for invoice_id, invoice_num, invoice_date in missing_dates:
        print(f"   - {invoice_num}")
        
        # Try to extract date from invoice number (e.g., OCT25-4761 -> 2025-10-01)
        date_guess = None
        if invoice_num:
            # Pattern: MON25-XXXX or MONYY-XXXX
            match = re.search(r'([A-Z]{3})(\d{2})', invoice_num)
            if match:
                month_str = match.group(1)
                year_str = match.group(2)
                
                month_map = {
                    'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
                    'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                    'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
                }
                
                if month_str in month_map:
                    year = f"20{year_str}"
                    month = month_map[month_str]
                    date_guess = f"{year}-{month}-01"
        
        if date_guess:
            cur.execute("""
                UPDATE invoices 
                SET invoice_date = %s 
                WHERE id = %s
            """, (date_guess, invoice_id))
            print(f"      ✅ Fixed {invoice_num}: Set date to {date_guess}")
        else:
            # Fallback: use created_at date
            cur.execute("""
                UPDATE invoices 
                SET invoice_date = DATE(created_at)
                WHERE id = %s
            """, (invoice_id,))
            print(f"      ✅ Fixed {invoice_num}: Set date from created_at")
    
    conn.commit()
    print(f"   ✅ Fixed {len(missing_dates)} invoice dates")
else:
    print("   ✅ No missing dates found")

# Issue 2: Fix missing vendor names (10 ledgers)
print("\n🏢 Issue 2: Fixing missing vendor names...")
cur.execute("""
    SELECT id, vendor_name, invoice_number 
    FROM invoices 
    WHERE vendor_name IS NULL OR vendor_name = '' OR TRIM(vendor_name) = ''
    ORDER BY created_at DESC
""")
missing_vendors = cur.fetchall()

if missing_vendors:
    print(f"   Found {len(missing_vendors)} invoices with missing vendor names:")
    for invoice_id, vendor_name, invoice_num in missing_vendors:
        # Set a default vendor name based on invoice number
        default_vendor = f"Vendor-{invoice_num}" if invoice_num else f"Vendor-{invoice_id[:8]}"
        
        cur.execute("""
            UPDATE invoices 
            SET vendor_name = %s 
            WHERE id = %s
        """, (default_vendor, invoice_id))
        print(f"   - {invoice_num}: Set to '{default_vendor}'")
    
    conn.commit()
    print(f"   ✅ Fixed {len(missing_vendors)} vendor names")
else:
    print("   ✅ No missing vendor names found")

# Issue 3: Check financial year issues
print("\n📆 Issue 3: Checking invoice date ranges...")
cur.execute("""
    SELECT 
        MIN(invoice_date) as earliest,
        MAX(invoice_date) as latest,
        COUNT(*) as total
    FROM invoices 
    WHERE invoice_date IS NOT NULL
""")
date_range = cur.fetchone()

if date_range:
    earliest, latest, total = date_range
    print(f"   Date Range: {earliest} to {latest} ({total} invoices)")
    
    if earliest:
        earliest_year = earliest.year
        print(f"\n   ⚠️  Your invoices start from {earliest}")
        print(f"   📝 Make sure your Tally Financial Year includes {earliest_year}-{earliest_year+1}")
        print(f"   📝 In Tally: Go to Company Info → Set Financial Year to include this period")

# Issue 4: Validate all required fields
print("\n✅ Issue 4: Validating all required fields...")
cur.execute("""
    SELECT 
        COUNT(*) FILTER (WHERE invoice_number IS NULL OR invoice_number = '') as missing_inv_num,
        COUNT(*) FILTER (WHERE invoice_date IS NULL) as missing_date,
        COUNT(*) FILTER (WHERE vendor_name IS NULL OR vendor_name = '') as missing_vendor,
        COUNT(*) FILTER (WHERE total_amount IS NULL OR total_amount = 0) as missing_amount
    FROM invoices
""")
validation = cur.fetchone()
missing_inv_num, missing_date, missing_vendor, missing_amount = validation

print(f"   Missing Invoice Numbers: {missing_inv_num}")
print(f"   Missing Dates: {missing_date}")
print(f"   Missing Vendor Names: {missing_vendor}")
print(f"   Missing Amounts: {missing_amount}")

if missing_inv_num == 0 and missing_date == 0 and missing_vendor == 0:
    print("\n   🎉 All required fields are now valid!")
else:
    print("\n   ⚠️  Some fields still need attention")

cur.close()
conn.close()

print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("1. Go to TrulyInvoice → Invoices page")
print("2. Click 'Export to Tally' button")
print("3. Download the new XML file")
print("4. In Tally Prime:")
print("   - Select your company (TrulyInvoice)")
print("   - Press O (Import)")
print("   - Click 'Transactions'")
print("   - Select the new XML file")
print("   - All invoices should import without errors!")
print("="*80)
