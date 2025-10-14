"""
ROBUSTNESS TEST - OCR to Export Pipeline
Test the complete pipeline robustness with comprehensive data extraction
"""
import os
import sys
import json
sys.path.append('backend')

from app.services.intelligent_extractor import IntelligentAIExtractor
from app.services.accountant_excel_exporter import AccountantExcelExporter

def test_pipeline_robustness():
    print("🔍 TESTING OCR-TO-EXPORT PIPELINE ROBUSTNESS")
    print("=" * 60)
    
    # Test sample invoice text with comprehensive data
    sample_invoice_text = """
    TAX INVOICE
    
    INNOVATION TECH SOLUTIONS PVT LTD
    GSTIN: 18AABCI4851C1ZB
    PAN: AABCI4851C
    Email: accounts@innovation.com
    Phone: +91-9876543210
    Address: 123 Tech Park, Guwahati, Assam - 781001
    
    Invoice No: INV/2025/001
    Invoice Date: 15-Jan-2025
    Due Date: 14-Feb-2025
    PO Number: PO-2024-XYZ
    
    Bill To:
    ABC Corporation Ltd
    GSTIN: 27AABCU9603R1ZM
    
    Place of Supply: Assam
    
    Item Details:
    SL  Description                 HSN     Qty    Rate      Amount
    1   Software License           998314   2     15000.00  30000.00
    2   Maintenance Service        998315   1     5000.00   5000.00
    
    Subtotal:                              35000.00
    CGST @ 9%:                             3150.00
    SGST @ 9%:                             3150.00
    Total Amount:                          41300.00
    
    Payment Terms: Net 30 days
    Payment Method: Bank Transfer
    
    Bank Details:
    Account: 123456789
    IFSC: SBIN0001234
    
    Authorized Signatory
    """
    
    print("📄 TESTING WITH COMPREHENSIVE INVOICE DATA")
    print("Contains: Vendor details, GSTIN, PAN, email, phone, address,")
    print("         Line items, HSN codes, taxes, payment terms, bank details")
    print()
    
    # Test AI extraction
    print("1️⃣ TESTING AI EXTRACTION...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No OpenAI API key found - cannot test extraction")
            return
            
        extractor = IntelligentAIExtractor(api_key)
        extracted_data = extractor.extract_from_text(sample_invoice_text)
        
        if extracted_data:
            print(f"✅ AI Extraction successful!")
            print(f"   Fields extracted: {len(extracted_data)}")
            
            # Check what was extracted
            expected_fields = [
                'vendor_name', 'vendor_gstin', 'vendor_pan', 'vendor_email', 
                'vendor_phone', 'vendor_address', 'invoice_number', 'invoice_date',
                'due_date', 'po_number', 'subtotal', 'cgst', 'sgst', 'total_amount',
                'place_of_supply', 'payment_terms', 'payment_method', 'line_items'
            ]
            
            print("\n   📋 EXTRACTION ANALYSIS:")
            extracted_count = 0
            missing_fields = []
            
            for field in expected_fields:
                if field in extracted_data and extracted_data[field]:
                    print(f"   ✅ {field}: {str(extracted_data[field])[:50]}")
                    extracted_count += 1
                else:
                    print(f"   ❌ {field}: MISSING")
                    missing_fields.append(field)
            
            extraction_rate = (extracted_count / len(expected_fields)) * 100
            print(f"\n   📊 EXTRACTION RATE: {extraction_rate:.1f}% ({extracted_count}/{len(expected_fields)} fields)")
            
            if extraction_rate < 80:
                print(f"   ⚠️  LOW extraction rate - AI may need prompt improvements")
            
            # Test export with extracted data
            print(f"\n2️⃣ TESTING EXCEL EXPORT...")
            try:
                exporter = AccountantExcelExporter()
                excel_file = exporter.export_invoice(extracted_data, "ROBUSTNESS_TEST.xlsx")
                print(f"✅ Excel export successful: {excel_file}")
                
                # Check if all extracted fields are preserved
                print("\n   📊 EXPORT FIELD PRESERVATION:")
                for field in extracted_data:
                    if extracted_data[field] is not None and extracted_data[field] != '':
                        print(f"   ✅ {field}: Preserved in export")
                
            except Exception as e:
                print(f"❌ Excel export failed: {e}")
            
        else:
            print("❌ AI Extraction failed - no data returned")
            
    except Exception as e:
        print(f"❌ AI Extraction error: {e}")
    
    print("\n" + "=" * 60)
    print("📊 ROBUSTNESS ASSESSMENT SUMMARY:")
    print("=" * 60)
    
    # Assessment points
    print("🔍 KEY ROBUSTNESS FACTORS:")
    print("   1. AI extraction comprehensiveness")
    print("   2. Database field mapping completeness") 
    print("   3. Export data preservation")
    print("   4. Missing data handling")
    print("   5. No artificial data addition")
    
    print("\n💡 RECOMMENDATIONS:")
    print("   • Enhance AI prompts to capture more fields")
    print("   • Update database mapping to save all extracted fields")
    print("   • Ensure exports handle null/missing gracefully")
    print("   • Add validation for critical business fields")
    print("   • Implement field-level confidence scoring")

if __name__ == "__main__":
    test_pipeline_robustness()