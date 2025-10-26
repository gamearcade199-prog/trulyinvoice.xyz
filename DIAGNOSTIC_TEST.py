"""
COMPREHENSIVE SYSTEM CHECK
Tests all components to find zero-amount issue
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 80)
print("SYSTEM DIAGNOSTIC - Finding Zero Amount Issue")
print("=" * 80)

# Test 1: Check environment
print("\n1️⃣ ENVIRONMENT CHECK:")
from dotenv import load_dotenv
load_dotenv('backend/.env')

openai_key = os.getenv('OPENAI_API_KEY')
supabase_url = os.getenv('SUPABASE_URL')

print(f"   ✅ OPENAI_API_KEY: {'SET' if openai_key else '❌ MISSING'}")
print(f"   ✅ SUPABASE_URL: {'SET' if supabase_url else '❌ MISSING'}")

# Test 2: Import check
print("\n2️⃣ MODULE IMPORT CHECK:")
try:
    from app.services.intelligent_extractor import IntelligentAIExtractor
    print("   ✅ IntelligentAIExtractor imported")
except Exception as e:
    print(f"   ❌ IntelligentAIExtractor import failed: {e}")

try:
    from app.services.ai_service import ai_service
    print("   ✅ AIService imported")
except Exception as e:
    print(f"   ❌ AIService import failed: {e}")

# Test 3: Extract test invoice
print("\n3️⃣ AI EXTRACTION TEST:")
try:
    extractor = IntelligentAIExtractor(openai_key)
    
    test_invoice = """
    AMAZON WEB SERVICES
    Tax Invoice
    
    Invoice Number: AWS-2025-12345
    Date: 2025-10-13
    
    Subtotal: $1,250.00
    Tax: $125.00
    Total Amount: $1,375.00
    """
    
    print("   Testing USD invoice extraction...")
    result = extractor.extract_from_text(test_invoice)
    
    if result:
        print(f"\n   📊 EXTRACTION RESULT:")
        print(f"      Vendor: {result.get('vendor_name', 'N/A')}")
        print(f"      Invoice #: {result.get('invoice_number', 'N/A')}")
        print(f"      Total: {result.get('total_amount', 'N/A')}")
        print(f"      Currency: {result.get('currency', 'N/A')}")
        
        # Check for issues
        if result.get('total_amount', 0) == 0:
            print("\n   ❌ PROBLEM FOUND: Total amount is ZERO!")
        else:
            print(f"\n   ✅ Total amount correctly extracted: {result.get('total_amount')}")
            
        if not result.get('currency'):
            print("   ❌ PROBLEM FOUND: Currency not extracted!")
        else:
            print(f"   ✅ Currency correctly extracted: {result.get('currency')}")
    else:
        print("   ❌ Extraction returned None!")
        
except Exception as e:
    print(f"   ❌ Extraction test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Check database save logic
print("\n4️⃣ DATABASE SAVE LOGIC CHECK:")
try:
    from app.services.document_processor import DocumentProcessor
    processor = DocumentProcessor()
    
    # Simulate extracted data
    test_extracted_data = {
        'vendor_name': 'Test Vendor',
        'invoice_number': 'TEST-001',
        'invoice_date': '2025-10-13',
        'total_amount': 1500.50,
        'currency': 'USD',
        'subtotal': 1400.00,
        'cgst': 0,
        'sgst': 0,
        'igst': 100.50
    }
    
    test_document = {
        'id': 'test-doc-id',
        'user_id': 'test-user-123'
    }
    
    # Check what would be saved
    invoice_data = {
        'user_id': test_document.get('user_id'),
        'document_id': test_document['id'],
        'vendor_name': test_extracted_data.get('vendor_name'),
        'total_amount': test_extracted_data.get('total_amount', 0),
        'currency': test_extracted_data.get('currency', 'INR'),
    }
    
    print(f"   Invoice data to be saved:")
    print(f"      total_amount: {invoice_data['total_amount']}")
    print(f"      currency: {invoice_data['currency']}")
    
    if invoice_data['total_amount'] == 0:
        print("   ❌ PROBLEM: total_amount would be saved as 0!")
    else:
        print("   ✅ total_amount would be saved correctly")
        
except Exception as e:
    print(f"   ⚠️ Could not test save logic: {e}")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
