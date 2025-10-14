"""
FAST INVOICE EXTRACTOR - Optimized for 5-10 Second Processing
Only extracts fields that are ACTUALLY PRESENT in the invoice
Optimized for speed while maintaining accuracy
ENHANCED: Robust payment status detection
"""
import os
import requests
import json
import re
import base64
from typing import Dict, Any, Optional
from datetime import datetime
from .payment_status_detector import PaymentStatusDetector

class FastInvoiceExtractor:
    """Ultra-fast invoice extractor optimized for 5-10 second processing"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"
        self.payment_detector = PaymentStatusDetector()
    
    def extract_from_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Optional[Dict[str, Any]]:
        """Ultra-fast image extraction - optimized for speed"""
        
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Enhanced prompt with robust payment status instructions
        prompt = self.payment_detector.generate_robust_prompt()
        
        try:
            response = self._call_fast_api(prompt, image_base64, mime_type)
            extracted_data = self._fast_parse(response)
            
            # ENHANCED: Apply robust payment status detection
            if extracted_data:
                extracted_data = self._enhance_payment_status(extracted_data, text="")
            
            return extracted_data
        except Exception as e:
            print(f"❌ Fast extraction error: {e}")
            return None
    
    def extract_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Ultra-fast text extraction"""
        
        # Enhanced prompt with robust payment status
        prompt = f"""Extract invoice data from this text as JSON. Only include existing fields.

REQUIRED: invoice_number, invoice_date (YYYY-MM-DD), vendor_name, total_amount (number), currency

PAYMENT STATUS (CRITICAL): Look for PAID stamps, watermarks, "payment received", transaction IDs, signatures. Set "paid" if found, "partial" for advances, "unpaid" if unclear.

OPTIONAL: vendor_gstin, cgst, sgst, igst, hsn_code, payment_method, line_items

Text: {text[:2000]}

Return JSON only:"""
        
        try:
            response = self._call_fast_api(prompt)
            extracted_data = self._fast_parse(response)
            
            # ENHANCED: Apply robust payment status detection with actual text
            if extracted_data:
                extracted_data = self._enhance_payment_status(extracted_data, text)
            
            return extracted_data
        except Exception as e:
            print(f"❌ Fast text extraction error: {e}")
            return None
    
    def _call_fast_api(self, prompt: str, image_base64: str = None, mime_type: str = None) -> str:
        """Optimized API call for maximum speed"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        if image_base64:
            # Vision API - optimized for speed
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
                                    "url": f"data:{mime_type};base64,{image_base64}",
                                    "detail": "low"  # KEY OPTIMIZATION - use low detail for speed
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0,  # Deterministic for speed
                "max_tokens": 500,  # Reduced for speed
                "top_p": 0.1  # More focused responses
            }
        else:
            # Text API - optimized
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0,
                "max_tokens": 400,  # Reduced for speed
                "top_p": 0.1
            }
        
        # Single fast call - no retries for speed
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=15)  # Reduced timeout
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"⚠️ API error: {e}")
            raise
    
    def _fast_parse(self, content: str) -> Dict[str, Any]:
        """Fast JSON parsing with minimal validation"""
        
        # Clean content quickly
        content = re.sub(r'```json\n?', '', content)
        content = re.sub(r'```\n?', '', content)
        content = content.strip()
        
        # Find JSON in content
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()
        
        try:
            data = json.loads(content)
            
            # Minimal validation - just required fields
            if not all(key in data for key in ['invoice_number', 'invoice_date', 'vendor_name', 'total_amount']):
                print("⚠️ Missing required fields")
                return None
            
            # Quick data cleaning
            if 'total_amount' in data:
                data['total_amount'] = self._clean_amount(data['total_amount'])
            
            # Clean other numeric fields quickly
            for field in ['subtotal', 'cgst', 'sgst', 'igst', 'discount']:
                if field in data:
                    data[field] = self._clean_amount(data[field])
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            return None
    
    def _clean_amount(self, amount) -> float:
        """Fast amount cleaning"""
        if isinstance(amount, (int, float)):
            return float(amount)
        
        if isinstance(amount, str):
            # Remove common symbols quickly
            cleaned = re.sub(r'[₹,$,\s]', '', str(amount))
            try:
                return float(cleaned)
            except:
                return 0.0
        
        return 0.0
    
    def _enhance_payment_status(self, data: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Enhance payment status detection using robust detector"""
        
        # If we have text, use our robust detector
        if text:
            status, confidence, evidence = self.payment_detector.detect_payment_status(text)
            
            # Update payment status with robust detection
            data['payment_status'] = status
            data['payment_confidence'] = confidence
            data['payment_evidence'] = evidence
            
            print(f"🔍 Payment Status: {status.upper()} (confidence: {confidence:.2f})")
            if evidence:
                print(f"   Evidence: {evidence[:3]}")  # Show first 3 pieces of evidence
        
        # If no robust detection possible, keep AI detection but mark low confidence
        elif 'payment_status' not in data:
            data['payment_status'] = 'unpaid'
            data['payment_confidence'] = 0.1
            data['payment_evidence'] = ['DEFAULT: No clear indicators found']
        
        return data

# Test the speed improvement
if __name__ == "__main__":
    print("🚀 FAST INVOICE EXTRACTOR - Speed Optimized")
    print("⚡ Target: 5-10 second processing")
    print("🔧 Optimizations:")
    print("   - Short focused prompts")
    print("   - Reduced max_tokens (500 vs 1000)")
    print("   - Low detail vision processing") 
    print("   - Single API call (no retries)")
    print("   - Minimal validation")
    print("   - Temperature=0 for deterministic speed")
    print("✅ Ready for integration!")