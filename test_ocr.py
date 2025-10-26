"""
Test the enhanced OCR on the invoice image
"""
import os
import sys
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
from app.services.intelligent_extractor import IntelligentAIExtractor
import json

# Load environment
load_dotenv('backend/.env')

# Initialize extractor
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY not found!")
    exit(1)

extractor = IntelligentAIExtractor(api_key)

# Test with sample invoice text (simulating the INNOVATION hotel invoice)
test_invoice = """
TAX INVOICE (Page 2)

INNOVATION - (from 1-Apr-25)
Jannath Hotel Bhupen Hazarika Setu Road & Snacks
Pattan Bazar, Guwahati 781001
GSTIN/UIN: 18AABCI4851C1ZB
State Name: Assam, Code: 18

Invoice No: IN67/2025-26
Invoice Date: 4-Jun-25
Mode/Terms of Payment: Dated
Delivery Note Date: 

Description of Goods    HSN/SAC   Quantity   Rate   Per   Disc %   Amount
Round Off                                                           (-) 0.01

                                                Total    1 NOS      ₹ 40,000.00
                                                                    E & O E

Amount Chargeable (in words)
INR Forty Thousand Only

                        Taxable      Rate      CGST         SGST/UTGST      Total
                        Value                 Amount   Rate  Amount    Tax Amount
95046000                33,898.31    9%    3,050.85   9%   3,050.85    6,101.70

Total                   33,898.31          3,050.85        3,050.85    6,101.70

Tax Amount (in words): INR Six Thousand One Hundred and Seventy paise Only

Declaration:
We declare that this invoice shows the actual price of
the goods described and that all particulars are true
and correct.

Company's Bank Details:
Bank Name: State Bank Of India
A/c No: 32838014480
Branch & IFS Code: Ulubari Branch & SBIN0005978
for INNOVATION - from 1-Apr-25

This is a Computer Generated Invoice
"""

print("=" * 80)
print("TESTING ENHANCED OCR")
print("=" * 80)

# Extract from text
print("\nExtracting from invoice text...")
result = extractor.extract_from_text(test_invoice)

if result:
    print("\nEXTRACTION SUCCESSFUL!\n")
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 80)
    print("KEY FIELDS CHECK:")
    print("=" * 80)
    print(f"Subtotal: Rs {result.get('subtotal', 0):,.2f}")
    print(f"CGST: Rs {result.get('cgst', 0):,.2f}")
    print(f"SGST: Rs {result.get('sgst', 0):,.2f}")
    print(f"Total: Rs {result.get('total_amount', 0):,.2f}")
    print(f"Payment Status: {result.get('payment_status', 'N/A')}")
    print(f"Line Items: {len(result.get('line_items', []))} items")
    
    if result.get('line_items'):
        print("\nLINE ITEMS:")
        for i, item in enumerate(result['line_items'], 1):
            print(f"  {i}. {item.get('description', 'N/A')} - Rs {item.get('amount', 0):,.2f}")
else:
    print("\n❌ Extraction failed!")

print("\n" + "=" * 80)
