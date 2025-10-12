"""
OPTIMIZED AI-based invoice extractor using OpenAI API
- Supports TEXT extraction from PDFs
- Supports IMAGE extraction (OCR) from JPG/PNG
- Works without httpx conflicts - uses requests library
- Production-ready with retry logic and error handling
"""
import os
import requests
import json
import re
import base64
from typing import Dict, Any, Optional, Union

class SimpleAIExtractor:
    """Extract invoice data using OpenAI (text + vision) without library conflicts"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.vision_model = "gpt-4o-mini"  # Supports vision
        self.text_model = "gpt-4o-mini"
    
    def extract_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract invoice data from text using OpenAI"""
        
        prompt = f"""
You are an expert invoice data extractor. Extract ALL information from this invoice.

Return ONLY valid JSON with these exact fields:
{{
    "invoice_number": "string (invoice/bill number, ID, or reference)",
    "invoice_date": "YYYY-MM-DD (convert any date format to this)",
    "vendor_name": "string (company/seller name)",
    "subtotal": 0.00,
    "cgst": 0.00,
    "sgst": 0.00,
    "igst": 0.00,
    "total_amount": 0.00
}}

CRITICAL RULES:
- Extract ACTUAL numbers from the invoice (no placeholders)
- Remove currency symbols (₹, $, Rs., INR, etc.)
- Remove commas from numbers (1,234.56 → 1234.56)
- If you see "Tax Invoice ID:" or similar, that's the invoice_number
- If CGST + SGST exist, set igst = 0
- If IGST exists, set cgst = 0 and sgst = 0
- If tax not mentioned, set all tax fields to 0
- Date formats: convert 01/09/2025, 2025-09-01, Sep 1 2025, etc. to YYYY-MM-DD
- Return ONLY the JSON, no markdown, no explanation

Invoice Text:
{text}
"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.text_model,
            "messages": [
                {"role": "system", "content": "You are a professional invoice data extractor. Always return valid JSON with actual extracted values, never use placeholders."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 800
        }
        
        try:
            # Retry logic for API calls
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"⚠️ API retry {attempt + 1}/{max_retries}: {e}")
                    continue
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Extract JSON from response (remove markdown code blocks if present)
            content = re.sub(r'```json\n?', '', content)
            content = re.sub(r'```\n?', '', content)
            content = content.strip()
            
            # Parse JSON
            invoice_data = json.loads(content)
            
            # Validate and clean data
            invoice_data = self._validate_and_clean(invoice_data)
            
            return invoice_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Response content: {content[:200]}")
            return None
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return None
    
    def extract_from_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Optional[Dict[str, Any]]:
        """Extract invoice data from IMAGE using OpenAI Vision (OCR)"""
        
        # Encode image to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """
You are an expert invoice OCR system. Extract ALL information from this invoice image.

Return ONLY valid JSON with these exact fields:
{
    "invoice_number": "string",
    "invoice_date": "YYYY-MM-DD",
    "vendor_name": "string",
    "subtotal": 0.00,
    "cgst": 0.00,
    "sgst": 0.00,
    "igst": 0.00,
    "total_amount": 0.00
}

CRITICAL RULES:
- Read ALL text from the image carefully
- Extract ACTUAL numbers (no placeholders like 10000 or 11800)
- Remove currency symbols and commas from numbers
- Convert any date format to YYYY-MM-DD
- If CGST + SGST exist, set igst = 0
- If IGST exists, set cgst = 0 and sgst = 0
- Return ONLY the JSON, no markdown, no explanation
"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.vision_model,
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
            "max_tokens": 800
        }
        
        try:
            # Retry logic
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = requests.post(self.base_url, headers=headers, json=payload, timeout=45)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"⚠️ Vision API retry {attempt + 1}/{max_retries}: {e}")
                    continue
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Extract JSON from response
            content = re.sub(r'```json\n?', '', content)
            content = re.sub(r'```\n?', '', content)
            content = content.strip()
            
            # Parse JSON
            invoice_data = json.loads(content)
            
            # Validate and clean
            invoice_data = self._validate_and_clean(invoice_data)
            
            print(f"✅ Image OCR successful: {invoice_data.get('vendor_name')} - ₹{invoice_data.get('total_amount')}")
            
            return invoice_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Vision API error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Vision JSON parse error: {e}")
            print(f"Response: {content[:200]}")
            return None
        except Exception as e:
            print(f"❌ Vision extraction error: {e}")
            return None
    
    def _validate_and_clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean extracted invoice data"""
        
        # Required fields
        required_fields = ['invoice_number', 'invoice_date', 'vendor_name', 'total_amount']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Ensure all numeric fields exist and are floats
        numeric_fields = ['subtotal', 'cgst', 'sgst', 'igst', 'total_amount']
        for field in numeric_fields:
            if field not in data:
                data[field] = 0.0
            else:
                # Clean numeric values
                value = str(data[field])
                value = value.replace(',', '')  # Remove commas
                value = re.sub(r'[₹$Rs\s]', '', value)  # Remove currency symbols
                data[field] = float(value)
        
        # Validate date format (YYYY-MM-DD)
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, data['invoice_date']):
            # Try to parse and convert common formats
            print(f"⚠️ Invalid date format: {data['invoice_date']}, using today")
            from datetime import datetime
            data['invoice_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Limit string lengths
        data['vendor_name'] = str(data['vendor_name'])[:50]
        data['invoice_number'] = str(data['invoice_number'])[:100]
        
        return data


# Test the extractor
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('backend/.env')
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Sample text from tax.pdf
    test_text = """
Tax invoice for Akib Hussain
Account ID: 720603707190037
Tax invoice ID: ADS438-104904172
Document date: 7 Sep 2025, 16:28
Transaction ID: 24445593195128386-24445593211795051

Paid: 1,895.68 INR
Subtotal: 1,606.51 INR
IGST (18%): 289.17 INR

Facebook India Online Services Pvt. Ltd.
GSTIN : 06AABCF5150G1ZZ
Invoice no. FBADS-438-104904172
    """
    
    extractor = SimpleAIExtractor(api_key)
    result = extractor.extract_from_text(test_text)
    
    if result:
        print("\n" + "=" * 70)
        print(" AI EXTRACTION RESULT")
        print("=" * 70)
        print(json.dumps(result, indent=2))
        print("\n✅ Extraction successful!")
    else:
        print("\n❌ Extraction failed")
