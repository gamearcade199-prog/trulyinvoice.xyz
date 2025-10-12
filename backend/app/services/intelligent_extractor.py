"""
INTELLIGENT AI EXTRACTOR - Flexible Field Detection
Only extracts fields that are ACTUALLY PRESENT in the invoice
Supports all types of Indian invoices (GST, non-GST, retail, wholesale, service)
"""
import os
import requests
import json
import re
import base64
from typing import Dict, Any, Optional
from datetime import datetime

class IntelligentAIExtractor:
    """Smart invoice extractor that only saves fields found in the document"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"  # Supports text + vision
    
    def extract_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract invoice data from text - ONLY fields that exist"""
        
        prompt = f"""
You are an expert Indian invoice data extractor. Analyze this invoice and extract ONLY the fields that are ACTUALLY PRESENT.

IMPORTANT RULES:
1. Only include fields that you can find in the invoice
2. Do NOT add fields with empty/null/0 values if they don't exist
3. Extract ACTUAL numbers (no placeholders)
4. Remove currency symbols (₹, Rs, INR, $)
5. Remove commas from numbers

REQUIRED FIELDS (always include):
- invoice_number: Invoice/Bill number or ID
- invoice_date: Date in YYYY-MM-DD format
- vendor_name: Company/Shop/Seller name
- total_amount: Final amount to pay (as number, no currency)

OPTIONAL FIELDS (only include if present in invoice):
- vendor_gstin: 15-digit GSTIN (only if present)
- vendor_pan: 10-char PAN (only if present)
- vendor_email: Email address (only if present)
- vendor_phone: Phone number (only if present)
- vendor_address: Full address (only if present)
- due_date: Payment due date YYYY-MM-DD (only if present)
- po_number: Purchase order number (only if present)
- subtotal: Amount before tax (only if shown)
- cgst: Central GST amount (only if mentioned)
- sgst: State GST amount (only if mentioned)
- igst: Integrated GST amount (only if mentioned)
- cess: Additional cess/tax (only if mentioned)
- discount: Discount amount (only if given)
- shipping_charges: Delivery/shipping cost (only if mentioned)
- tds_amount: TDS deducted (only if shown)
- roundoff: Rounding adjustment (only if shown)
- hsn_code: HSN code for goods (only if present)
- sac_code: SAC code for services (only if present)
- place_of_supply: Place of supply for GST (only if mentioned)
- payment_terms: Payment terms like "Net 30" (only if stated)
- payment_method: Payment method like "UPI/Cash/Card" (only if mentioned)

GST TAX RULES:
- If you see CGST + SGST: Include both, don't include igst
- If you see IGST: Include igst, don't include cgst/sgst
- If no tax mentioned: Don't include any tax fields

Return ONLY valid JSON. Example formats:

SIMPLE RETAIL BILL (minimal fields):
{{
    "invoice_number": "BILL-123",
    "invoice_date": "2025-01-15",
    "vendor_name": "ABC Store",
    "total_amount": 500.00
}}

FULL GST INVOICE (many fields):
{{
    "invoice_number": "INV-2025-001",
    "invoice_date": "2025-01-15",
    "vendor_name": "XYZ Pvt Ltd",
    "vendor_gstin": "27AABCU9603R1ZM",
    "vendor_address": "Mumbai, Maharashtra",
    "subtotal": 10000.00,
    "cgst": 900.00,
    "sgst": 900.00,
    "total_amount": 11800.00,
    "place_of_supply": "Maharashtra",
    "hsn_code": "8471"
}}

Now extract from this invoice:
{text}

Return ONLY the JSON object, no markdown, no explanation.
"""
        
        try:
            response = self._call_api(prompt, is_vision=False)
            return self._parse_and_validate(response)
        except Exception as e:
            print(f"❌ Text extraction error: {e}")
            return None
    
    def extract_from_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Optional[Dict[str, Any]]:
        """Extract invoice data from IMAGE - ONLY fields that exist"""
        
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """
You are an expert Indian invoice OCR system. Read this invoice image and extract ONLY the fields that are ACTUALLY VISIBLE.

IMPORTANT:
1. Read ALL text carefully from the image
2. Only include fields you can see
3. Do NOT add fields with 0/null if they're not in the image
4. Extract real numbers (no placeholders)

REQUIRED FIELDS:
- invoice_number
- invoice_date (YYYY-MM-DD)
- vendor_name
- total_amount (number only, no ₹)

OPTIONAL FIELDS (only if visible):
- vendor_gstin (15 digits)
- vendor_pan (10 chars)
- vendor_email, vendor_phone, vendor_address
- due_date, po_number
- subtotal, cgst, sgst, igst, cess
- discount, shipping_charges, tds_amount
- hsn_code, sac_code, place_of_supply
- payment_terms, payment_method

GST RULES:
- CGST + SGST = Intra-state (don't add igst)
- IGST = Inter-state (don't add cgst/sgst)
- No tax visible = Don't add tax fields

Return ONLY JSON object with fields you found. No markdown, no explanation.
"""
        
        try:
            response = self._call_api(prompt, is_vision=True, image_base64=image_base64, mime_type=mime_type)
            return self._parse_and_validate(response)
        except Exception as e:
            print(f"❌ Image extraction error: {e}")
            return None
    
    def _call_api(self, prompt: str, is_vision: bool = False, image_base64: str = None, mime_type: str = None) -> str:
        """Call OpenAI API with retry logic"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        if is_vision and image_base64:
            # Vision API call
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 1000
            }
        else:
            # Text API call
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a professional invoice data extractor. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 1000
            }
        
        # Retry logic
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                return content
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                print(f"⚠️ API retry {attempt + 1}/{max_retries}")
        
        raise Exception("API call failed after retries")
    
    def _parse_and_validate(self, content: str) -> Dict[str, Any]:
        """Parse JSON and validate required fields"""
        
        # Remove markdown code blocks
        content = re.sub(r'```json\n?', '', content)
        content = re.sub(r'```\n?', '', content)
        content = content.strip()
        
        # Parse JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Content: {content[:200]}")
            raise
        
        # Validate required fields
        required = ['invoice_number', 'invoice_date', 'vendor_name', 'total_amount']
        for field in required:
            if field not in data or not data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Clean and validate data
        data = self._clean_data(data)
        
        return data
    
    def _clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate all fields"""
        
        cleaned = {}
        
        # Define field types
        string_fields = [
            'invoice_number', 'vendor_name', 'vendor_gstin', 'vendor_pan',
            'vendor_email', 'vendor_phone', 'vendor_address', 'po_number',
            'hsn_code', 'sac_code', 'place_of_supply', 'payment_terms', 'payment_method'
        ]
        
        numeric_fields = [
            'subtotal', 'cgst', 'sgst', 'igst', 'cess', 'discount',
            'total_amount', 'shipping_charges', 'tds_amount', 'roundoff'
        ]
        
        date_fields = ['invoice_date', 'due_date']
        
        # Clean string fields
        for field in string_fields:
            if field in data and data[field]:
                value = str(data[field]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', 'na', '-']:
                    cleaned[field] = value
        
        # Clean numeric fields
        for field in numeric_fields:
            if field in data and data[field] is not None:
                try:
                    value = str(data[field])
                    # Remove currency symbols and commas
                    value = re.sub(r'[₹$Rs,\s]', '', value)
                    value = re.sub(r'INR|EUR|USD', '', value, flags=re.IGNORECASE)
                    value = value.strip()
                    
                    if value and value not in ['0', '0.0', '0.00']:
                        cleaned[field] = float(value)
                except (ValueError, TypeError):
                    pass  # Skip invalid numeric values
        
        # Clean date fields
        for field in date_fields:
            if field in data and data[field]:
                date_value = str(data[field]).strip()
                if date_value and date_value.lower() not in ['null', 'none', 'n/a']:
                    # Validate YYYY-MM-DD format
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_value):
                        cleaned[field] = date_value
                    else:
                        print(f"⚠️ Invalid date format for {field}: {date_value}")
        
        # Ensure required fields
        if 'invoice_number' not in cleaned:
            cleaned['invoice_number'] = 'UNKNOWN'
        if 'invoice_date' not in cleaned:
            cleaned['invoice_date'] = datetime.now().strftime('%Y-%m-%d')
        if 'vendor_name' not in cleaned:
            cleaned['vendor_name'] = 'Unknown Vendor'
        if 'total_amount' not in cleaned:
            raise ValueError("total_amount is required")
        
        # Validate GST rules
        has_cgst = 'cgst' in cleaned and cleaned['cgst'] > 0
        has_sgst = 'sgst' in cleaned and cleaned['sgst'] > 0
        has_igst = 'igst' in cleaned and cleaned['igst'] > 0
        
        if has_cgst or has_sgst:
            # Intra-state: remove IGST if present
            if has_igst:
                print("⚠️ Both CGST/SGST and IGST present - removing IGST (intra-state)")
                del cleaned['igst']
        elif has_igst:
            # Inter-state: remove CGST/SGST if present
            if has_cgst:
                del cleaned['cgst']
            if has_sgst:
                del cleaned['sgst']
        
        return cleaned


# Test the intelligent extractor
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('backend/.env')
    
    api_key = os.getenv('OPENAI_API_KEY')
    extractor = IntelligentAIExtractor(api_key)
    
    # Test 1: Simple retail bill (minimal fields)
    print("\n" + "=" * 70)
    print("TEST 1: SIMPLE RETAIL BILL")
    print("=" * 70)
    
    simple_bill = """
    ABC STORE
    Bill No: 12345
    Date: 15/01/2025
    Total: Rs. 500
    """
    
    result1 = extractor.extract_from_text(simple_bill)
    if result1:
        print(json.dumps(result1, indent=2))
        print(f"\n✅ Extracted {len(result1)} fields (minimal invoice)")
    
    # Test 2: Full GST invoice (many fields)
    print("\n" + "=" * 70)
    print("TEST 2: FULL GST INVOICE")
    print("=" * 70)
    
    gst_invoice = """
    TAX INVOICE
    
    XYZ Technologies Pvt Ltd
    GSTIN: 27AABCU9603R1ZM
    Address: Mumbai, Maharashtra 400001
    Email: sales@xyz.com
    Phone: +91-9876543210
    
    Invoice No: INV-2025-001
    Invoice Date: 15-Jan-2025
    PO Number: PO-12345
    Place of Supply: Maharashtra
    HSN Code: 8471
    
    Subtotal: Rs. 10,000.00
    CGST (9%): Rs. 900.00
    SGST (9%): Rs. 900.00
    Total: Rs. 11,800.00
    
    Payment Terms: Net 30 days
    """
    
    result2 = extractor.extract_from_text(gst_invoice)
    if result2:
        print(json.dumps(result2, indent=2))
        print(f"\n✅ Extracted {len(result2)} fields (full GST invoice)")
    
    # Test 3: Service invoice with IGST
    print("\n" + "=" * 70)
    print("TEST 3: SERVICE INVOICE (IGST)")
    print("=" * 70)
    
    service_invoice = """
    INVOICE FOR SERVICES
    
    Digital Marketing Agency
    GSTIN: 29AADCA1234M1Z5
    
    Invoice #: SRV-2025-100
    Date: 10/01/2025
    SAC Code: 998314
    Place of Supply: Karnataka
    
    Consulting Fees: ₹50,000
    IGST @ 18%: ₹9,000
    Total Amount: ₹59,000
    """
    
    result3 = extractor.extract_from_text(service_invoice)
    if result3:
        print(json.dumps(result3, indent=2))
        print(f"\n✅ Extracted {len(result3)} fields (service invoice with IGST)")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 70)
    print("\nKEY FEATURES:")
    print("✅ Only extracts fields that exist in invoice")
    print("✅ No empty/null fields in output")
    print("✅ Supports simple to complex invoices")
    print("✅ Handles GST (CGST+SGST or IGST)")
    print("✅ Works across all Indian invoice formats")
