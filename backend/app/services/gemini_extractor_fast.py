"""
🚀 ULTRA-FAST GEMINI 2.5 FLASH EXTRACTOR
Single-pass, maximum accuracy, minimal tokens
"""

import os
import json
import base64
import hashlib
import re
from datetime import datetime
from typing import Dict, Any, Optional
import google.generativeai as genai


class GeminiExtractor:
    def __init__(self):
        """Initialize Gemini 2.5 Flash for ultra-fast extraction"""
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        # Use production model
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.model = genai.GenerativeModel(self.model_name)
        
        print(f"✅ GEMINI 2.5 FLASH extraction ENABLED - 95% accuracy target")

    def extract_from_text(self, text: str, original_filename: str = "unknown.txt") -> Optional[Dict[str, Any]]:
        """🚀 ULTRA-FAST text extraction - single pass"""
        print(f"\n{'='*60}")
        print(f"⚡ GEMINI 2.5 FLASH - LIGHTNING EXTRACTION")
        print(f"{'='*60}")
        
        result = self._extract_invoice_data(text, is_vision=False)
        return self._finalize_result(result, original_filename)

    def extract_from_image(self, image_path: str = None, image_base64: str = None, 
                          mime_type: str = "image/jpeg", original_filename: str = "unknown.jpg") -> Optional[Dict[str, Any]]:
        """🚀 ULTRA-FAST image extraction - single pass"""
        print(f"\n{'='*60}")
        print(f"⚡ GEMINI 2.5 FLASH - LIGHTNING EXTRACTION")
        print(f"{'='*60}")
        
        # Handle image input
        if image_path:
            with open(image_path, 'rb') as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        if not image_base64:
            print("  ❌ No image data provided")
            return None
            
        result = self._extract_invoice_data(None, is_vision=True, image_base64=image_base64, mime_type=mime_type)
        return self._finalize_result(result, original_filename, extraction_type='vision_ocr')

    def _extract_invoice_data(self, text: str = None, is_vision: bool = False, 
                             image_base64: str = None, mime_type: str = None) -> Optional[Dict[str, Any]]:
        """🚀 SINGLE ULTRA-OPTIMIZED EXTRACTION"""
        
        prompt = """🏆 WORLD-CLASS INDIAN INVOICE EXTRACTION AI - 99% ACCURACY

TASK: Extract ALL invoice data with CONFIDENCE SCORES (0.0 to 1.0) in ONE SHOT.

🎯 CRITICAL RULES:
1. Extract ONLY fields that exist in the invoice
2. For EACH field, provide confidence score
3. Extract ALL line items from tables
4. Detect currency from symbols (₹=INR, $=USD, €=EUR)
5. Remove currency symbols and commas from amounts
6. Use YYYY-MM-DD format for dates

📋 REQUIRED FIELDS (with confidence):
- invoice_number, invoice_number_confidence
- invoice_date, invoice_date_confidence
- vendor_name, vendor_name_confidence
- total_amount (numeric), total_amount_confidence
- currency, currency_confidence

🔢 OPTIONAL FIELDS (only if visible, with confidence):
- vendor_gstin, vendor_gstin_confidence
- vendor_pan, vendor_pan_confidence
- vendor_email, vendor_email_confidence
- vendor_phone, vendor_phone_confidence
- vendor_address, vendor_address_confidence
- customer_name, customer_name_confidence
- customer_address, customer_address_confidence
- subtotal, subtotal_confidence
- cgst, cgst_confidence
- sgst, sgst_confidence
- igst, igst_confidence
- taxable_value, taxable_value_confidence
- tax_amount, tax_amount_confidence
- hsn_code, hsn_code_confidence
- bank_name, bank_name_confidence
- account_number, account_number_confidence
- ifsc_code, ifsc_code_confidence
- payment_status, payment_status_confidence

📊 LINE ITEMS (extract ALL):
For each item in table:
{
  "description": "Item name",
  "quantity": number,
  "rate": number,
  "amount": number,
  "hsn_sac": "code if visible",
  "confidence": 0.95
}

⚠️ CONFIDENCE GUIDE:
- 1.0: Perfectly clear, no doubt
- 0.95: Very clear, minor formatting
- 0.90: Clear with small uncertainty
- 0.85: Readable but slightly ambiguous
- 0.80: Partially visible/unclear
- <0.80: Very unclear or missing

📋 OUTPUT FORMAT (STRICT JSON):
{
  "invoice_number": "INV-001",
  "invoice_number_confidence": 0.98,
  "vendor_name": "Company Ltd",
  "vendor_name_confidence": 0.95,
  "total_amount": 40000.00,
  "total_amount_confidence": 1.0,
  "currency": "INR",
  "currency_confidence": 1.0,
  "line_items": [
    {
      "description": "Service",
      "quantity": 1,
      "rate": 40000,
      "amount": 40000,
      "confidence": 0.95
    }
  ],
  "payment_status": "unpaid",
  "payment_status_confidence": 1.0
}

🚨 CRITICAL:
- Return ONLY valid JSON
- Include confidence for ALL fields
- Remove currency symbols (₹, Rs, $)
- Extract ALL visible line items
- Be thorough but fast

""" + ("Invoice text:\n" + text if text else "Analyze the invoice image:")

        try:
            print(f"🔥 Single-pass extraction...")
            
            if is_vision:
                # Vision API call
                response = self.model.generate_content([
                    prompt,
                    {
                        "mime_type": mime_type,
                        "data": image_base64
                    }
                ])
            else:
                # Text API call
                response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                print("  ❌ No response from Gemini")
                return None
            
            # Parse JSON response
            result_text = response.text.strip()
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
            
            result = json.loads(result_text)
            
            # Quick validation fix for common issues
            result = self._quick_validate_fix(result)
            
            print(f"   ✅ Extracted {len([k for k in result.keys() if not k.endswith('_confidence')])} fields")
            return result
            
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON parsing error: {e}")
            return None
        except Exception as e:
            print(f"  ❌ Extraction error: {e}")
            return None

    def _quick_validate_fix(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Quick validation and auto-fix common issues"""
        
        # Fix GSTIN format if present
        if 'vendor_gstin' in result:
            gstin = str(result['vendor_gstin']).upper().replace(' ', '')
            if len(gstin) == 15 and gstin.isalnum():
                result['vendor_gstin'] = gstin
            elif len(gstin) != 15 or not gstin.isalnum():
                if 'vendor_gstin_confidence' in result:
                    result['vendor_gstin_confidence'] = min(0.7, result['vendor_gstin_confidence'])
        
        # Ensure payment_status defaults
        if 'payment_status' not in result:
            result['payment_status'] = 'unpaid'
            result['payment_status_confidence'] = 1.0
        
        # Ensure currency is detected
        if 'currency' not in result and 'total_amount' in result:
            result['currency'] = 'INR'  # Default for Indian invoices
            result['currency_confidence'] = 0.9
        
        return result

    def _finalize_result(self, result: Optional[Dict[str, Any]], original_filename: str, extraction_type: str = 'text') -> Optional[Dict[str, Any]]:
        """Add metadata and generate quality report"""
        if not result:
            return None
        
        # Add metadata
        overall_confidence = self._calculate_overall_confidence(result)
        result['_extraction_hash'] = self._generate_hash(result)
        result['_extraction_metadata'] = {
            'extraction_date': datetime.now().isoformat(),
            'model': self.model_name,
            'extraction_type': extraction_type,
            'passes_completed': 1,  # Single pass
            'overall_confidence': overall_confidence,
            'original_filename': original_filename,
            'quality_grade': self._get_quality_grade(overall_confidence)
        }
        
        # Print quality report
        self._print_quality_report(result)
        
        return result

    def _calculate_overall_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate overall confidence from all confidence scores"""
        confidence_scores = []
        
        for key, value in data.items():
            if key.endswith('_confidence') and isinstance(value, (int, float)):
                confidence_scores.append(float(value))
        
        if not confidence_scores:
            return 0.5  # Default if no confidence scores found
        
        return sum(confidence_scores) / len(confidence_scores)

    def _get_quality_grade(self, confidence: float) -> str:
        """Get quality grade based on confidence"""
        if confidence >= 0.95:
            return "EXCELLENT"
        elif confidence >= 0.90:
            return "VERY_GOOD"
        elif confidence >= 0.85:
            return "GOOD"
        elif confidence >= 0.80:
            return "FAIR"
        else:
            return "NEEDS_REVIEW"

    def _generate_hash(self, data: Dict[str, Any]) -> str:
        """Generate hash for duplicate detection"""
        # Create hash from key invoice fields
        hash_fields = ['invoice_number', 'vendor_name', 'total_amount', 'invoice_date']
        hash_data = {}
        
        for field in hash_fields:
            if field in data:
                hash_data[field] = data[field]
        
        hash_string = json.dumps(hash_data, sort_keys=True, default=str)
        return hashlib.md5(hash_string.encode()).hexdigest()

    def _print_quality_report(self, result: Dict[str, Any]):
        """Print quality report"""
        metadata = result.get('_extraction_metadata', {})
        confidence = metadata.get('overall_confidence', 0)
        grade = metadata.get('quality_grade', 'UNKNOWN')
        
        print(f"\n{'='*60}")
        print(f"📊 GEMINI QUALITY REPORT")
        print(f"{'='*60}")
        print(f"🎯 Overall Confidence: {confidence:.1%}")
        print(f"🏅 Quality Grade: {grade}")
        
        if grade == "EXCELLENT":
            print(f"   ✅ EXCELLENT - Production ready")
        elif grade == "VERY_GOOD":
            print(f"   ✅ VERY GOOD - Minor review needed")
        elif grade == "GOOD":
            print(f"   ⚠️ GOOD - Some fields need review")
        else:
            print(f"   ⚠️ {grade} - Multiple fields need review")
        
        # Show low confidence fields
        low_confidence_fields = []
        for key, value in result.items():
            if key.endswith('_confidence') and isinstance(value, (int, float)) and value < 0.85:
                field_name = key.replace('_confidence', '')
                low_confidence_fields.append(f"   - {field_name}: {value:.1%}")
        
        if low_confidence_fields:
            print(f"\n⚠️ {len(low_confidence_fields)} fields need review:")
            for field in low_confidence_fields:
                print(field)
        
        # Count extracted fields and line items
        field_count = len([k for k in result.keys() if not k.endswith('_confidence') and not k.startswith('_')])
        line_items = result.get('line_items', [])
        
        print(f"\n📋 Total fields extracted: {field_count}")
        print(f"📊 Line items extracted: {len(line_items)}")
        
        # Show key extracted data
        vendor = result.get('vendor_name', 'Unknown')
        amount = result.get('total_amount', 0)
        currency = result.get('currency', 'INR')
        
        if vendor and amount:
            print(f"\n✅ AI extracted: {vendor} - {currency} {amount:,.2f}")
        
        print(f"{'='*60}")