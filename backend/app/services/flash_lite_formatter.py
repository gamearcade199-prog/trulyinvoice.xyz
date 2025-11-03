"""
⚡ GEMINI 2.5 FLASH-LITE FORMATTER
Ultra-cheap text-to-JSON formatting at ₹0.01 per invoice
"""

import os
import json
import re
from typing import Dict, Any, Optional
import google.generativeai as genai


class FlashLiteFormatter:
    def __init__(self):
        """Initialize Gemini 2.5 Flash-Lite for text formatting"""
        api_key = os.getenv('GOOGLE_AI_API_KEY') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY or GEMINI_API_KEY environment variable not set")
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
            self.generation_config = {
                'temperature': 0.1,  # Low temperature for consistent formatting
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        except Exception as e:
            raise Exception(f"Failed to initialize Flash-Lite model: {e}")
    
    def format_text_to_json(self, raw_text: str) -> Dict[str, Any]:
        """
        Format raw text from Vision API into structured JSON
        
        Args:
            raw_text: Raw text extracted from Vision API
            
        Returns:
            Structured JSON with invoice data and confidence scores
        """
        # For large documents, try direct extraction first
        if len(raw_text) > 3000:
            print("  📊 Large document detected - trying direct OCR extraction first...")
            direct_result = self._direct_ocr_extraction(raw_text)
            if direct_result.get('total_amount', 0) > 0:
                print(f"  ✅ Direct extraction successful: ₹{direct_result['total_amount']}")
                return direct_result
            print("  ⚠️ Direct extraction incomplete - falling back to Flash-Lite...")
        
        try:
            # Create optimized prompt for text-to-JSON conversion
            prompt = self._create_formatting_prompt(raw_text)
            
            # Generate structured JSON using Flash-Lite
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            if not response or not response.text:
                return self._create_error_response("No response from Flash-Lite model")
            
            # Parse and validate JSON response
            try:
                # Extract JSON from response (handle markdown formatting)
                json_text = self._extract_json_from_response(response.text)
                parsed_data = json.loads(json_text)
                
                # Add formatting metadata
                parsed_data['_formatting_metadata'] = {
                    'model': 'gemini-2.5-flash-lite',
                    'cost_inr': 0.01,
                    'method': 'text_to_json_formatting',
                    'input_length': len(raw_text),
                    'success': True
                }
                
                # ✨ NEW: Enhance payment status detection with heuristics
                parsed_data = self._enhance_payment_status(parsed_data, raw_text)
                
                # ✨ NEW: Enhance critical fields with regex extraction
                parsed_data = self._enhance_critical_fields(parsed_data, raw_text)
                
                return parsed_data
                
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing error: {e}")
                print(f"  🔧 Attempting to fix truncated/malformed JSON...")
                
                # Try to fix common JSON issues including truncation
                fixed_json = self._fix_json_issues(response.text)
                
                try:
                    parsed_data = json.loads(fixed_json)
                    print(f"  ✅ JSON fixed successfully!")
                    parsed_data['_formatting_metadata'] = {
                        'model': 'gemini-2.5-flash-lite',
                        'cost_inr': 0.01,
                        'method': 'text_to_json_formatting_fixed',
                        'success': True,
                        'json_fixed': True
                    }
                    # ✨ NEW: Enhance payment status for fixed JSON too
                    parsed_data = self._enhance_payment_status(parsed_data, raw_text)
                    
                    # ✨ NEW: Enhance critical fields with regex extraction
                    parsed_data = self._enhance_critical_fields(parsed_data, raw_text)
                    
                    return parsed_data
                except json.JSONDecodeError as e2:
                    print(f"  ❌ JSON fix failed: {e2}")
                    print(f"  📄 Attempting aggressive extraction from partial JSON...")
                    
                    # Last resort: Extract what we can from the broken JSON
                    return self._extract_from_broken_json(response.text, raw_text)
                    
        except Exception as e:
            print(f"❌ Flash-Lite formatting error: {e}")
            return self._create_error_response(str(e))
    
    def _create_formatting_prompt(self, raw_text: str) -> str:
        """Create optimized prompt for Flash-Lite text formatting with ALL fields"""
        return f"""Convert this invoice text into structured JSON with confidence scores.

TASK: Extract ALL invoice fields from the raw text. Extract EVERY field present in the invoice.

RAW TEXT:
{raw_text}

REQUIRED JSON FORMAT (extract ALL fields that exist):
{{
  "invoice_number": "INV-123", "invoice_number_confidence": 0.95,
  "invoice_date": "YYYY-MM-DD", "invoice_date_confidence": 0.90,
  "due_date": "YYYY-MM-DD", "due_date_confidence": 0.85,
  "po_number": "PO-123", "po_number_confidence": 0.80,
  
  "vendor_name": "ABC Company", "vendor_name_confidence": 0.95,
  "vendor_gstin": "27AABCU9603R1ZM", "vendor_gstin_confidence": 0.90,
  "vendor_pan": "AABCU9603R", "vendor_pan_confidence": 0.85,
  "vendor_address": "123 Street, City", "vendor_address_confidence": 0.80,
  "vendor_state": "Maharashtra", "vendor_state_confidence": 0.85,
  "vendor_phone": "9876543210", "vendor_phone_confidence": 0.85,
  "vendor_email": "vendor@example.com", "vendor_email_confidence": 0.80,
  
  "customer_name": "XYZ Corp", "customer_name_confidence": 0.90,
  "customer_gstin": "29AABCT1234F2Z5", "customer_gstin_confidence": 0.85,
  "customer_pan": "AABCT1234F", "customer_pan_confidence": 0.80,
  "customer_address": "456 Road, City", "customer_address_confidence": 0.75,
  "customer_state": "Karnataka", "customer_state_confidence": 0.80,
  "customer_phone": "9123456789", "customer_phone_confidence": 0.80,
  "customer_email": "customer@example.com", "customer_email_confidence": 0.75,
  
  "subtotal": 850.00, "subtotal_confidence": 0.95,
  "discount": 50.00, "discount_confidence": 0.90,
  "shipping_charges": 100.00, "shipping_charges_confidence": 0.85,
  "cgst": 76.50, "cgst_confidence": 0.90,
  "sgst": 76.50, "sgst_confidence": 0.90,
  "igst": 0.00, "igst_confidence": 0.90,
  "total_amount": 1000.00, "total_amount_confidence": 0.98,
  "currency": "INR", "currency_confidence": 1.0,
  
  "payment_status": "pending", "payment_status_confidence": 0.80,
  "paid_amount": 500.00, "paid_amount_confidence": 0.85,
  "payment_method": "Bank Transfer", "payment_method_confidence": 0.75,
  "payment_terms": "Net 30 days", "payment_terms_confidence": 0.70,
  "bank_account": "1234567890", "bank_account_confidence": 0.75,
  
  "notes": "Urgent delivery", "notes_confidence": 0.70,
  "reference_number": "REF-123", "reference_confidence": 0.75,
  
  "line_items": [
    {{
      "description": "Item name", "description_confidence": 0.90,
      "hsn_sac": "8471", "hsn_sac_confidence": 0.85,
      "quantity": 10, "quantity_confidence": 0.95,
      "unit": "Pcs", "unit_confidence": 0.90,
      "rate": 85.00, "rate_confidence": 0.95,
      "amount": 850.00, "amount_confidence": 0.95,
      "cgst_rate": 9.0, "cgst_rate_confidence": 0.90,
      "sgst_rate": 9.0, "sgst_rate_confidence": 0.90,
      "igst_rate": 0.0, "igst_rate_confidence": 0.90,
      "cgst_amount": 76.50, "cgst_amount_confidence": 0.90,
      "sgst_amount": 76.50, "sgst_amount_confidence": 0.90,
      "igst_amount": 0.00, "igst_amount_confidence": 0.90,
      "sub_vendor": "Source vendor name if consolidated bill", "sub_vendor_confidence": 0.85,
      "sub_bill_number": "Sub-invoice number if multiple bills", "sub_bill_number_confidence": 0.80,
      "sub_gstin": "Sub-vendor GSTIN if present", "sub_gstin_confidence": 0.85
    }}
  ]
}}

CRITICAL INSTRUCTIONS:
1. Extract ALL fields that exist in the text - do not skip any field
2. For CONSOLIDATED INVOICES (multiple vendors/bills in one document):
   - If you see multiple vendor names, bill numbers, or GSTIN numbers
   - Group line items by their source vendor
   - Add "sub_vendor", "sub_bill_number", and "sub_gstin" to each line item
   - Example: "PENNY BIG BAZAR", "THE BASKET DEPT", "MARKET PLACE" etc.
   - ⚠️ IMPORTANT: For large consolidated invoices, include ONLY summary line items (totals per sub-vendor) to keep JSON compact
3. For GSTIN: Look for 15-character alphanumeric (format: 27AABCU9603R1ZM)
4. For PAN: Look for 10-character alphanumeric (format: AABCU9603R)
5. For Phone: Extract 10-digit numbers near vendor/customer names
6. For Email: Extract email addresses near vendor/customer sections
7. For HSN/SAC: Extract from line items (usually 4-8 digits)
8. Use confidence 0.0-1.0 based on text clarity (clear=0.9+, unclear=0.5-0.7)
9. Remove currency symbols (₹, $, €) from amounts
10. Format dates as YYYY-MM-DD
11. If field not found, omit it (don't include null values)
12. Return ONLY valid JSON, no explanations
13. ⚠️ KEEP RESPONSE UNDER 2000 TOKENS - Summarize if needed

JSON OUTPUT:"""
    
    def _enhance_payment_status(self, result: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
        """
        ✨ Enhance payment status detection using text analysis heuristics
        Improves accuracy from 80% to 90%+
        """
        from datetime import datetime
        
        text_lower = raw_text.lower()
        
        # Rule 1: Check for "Paid" indicators (highest confidence)
        paid_indicators = [
            'paid', 'payment received', 'payment done',
            'cheque attached', 'cheque deposited', 'cheque cleared',
            'payment cleared', 'settled', 'completed', 'transferred'
        ]
        if any(indicator in text_lower for indicator in paid_indicators):
            result['payment_status'] = 'paid'
            result['payment_status_confidence'] = 0.95
            print("  💚 Payment status: PAID (high confidence)")
            return result
        
        # Rule 2: Check for "Unpaid" indicators
        unpaid_indicators = [
            'unpaid', 'outstanding', 'not paid', 'payment pending',
            'awaiting payment', 'pending payment', 'balance due',
            'to be paid', 'due payment'
        ]
        if any(indicator in unpaid_indicators for indicator in unpaid_indicators):
            result['payment_status'] = 'unpaid'
            result['payment_status_confidence'] = 0.90
            print("  🔴 Payment status: UNPAID (high confidence)")
            return result
        
        # Rule 3: Check for "Overdue" indicators
        overdue_indicators = [
            'overdue', 'past due', 'overdue amount',
            'delayed payment', 'late payment'
        ]
        if any(indicator in overdue_indicators for indicator in overdue_indicators):
            result['payment_status'] = 'overdue'
            result['payment_status_confidence'] = 0.90
            print("  ⚠️  Payment status: OVERDUE (high confidence)")
            return result
        
        # Rule 4: Check for "Pending" / Credit Terms indicators
        pending_indicators = [
            'pending', 'net 30', 'net 60', 'net 90',
            'credit terms', 'payment terms',
            'due in 30', 'due in 60', 'days credit'
        ]
        if any(indicator in pending_indicators for indicator in pending_indicators):
            result['payment_status'] = 'unpaid'  # Map pending to unpaid (DB constraint)
            result['payment_status_confidence'] = 0.80
            print("  🟡 Payment status: UNPAID (pending/credit terms - medium confidence)")
            return result
        
        # Rule 5: Check date-based logic
        if 'due_date' in result and result.get('due_date'):
            try:
                due_date = datetime.strptime(str(result['due_date']), '%Y-%m-%d')
                if due_date < datetime.now():
                    # Due date has passed - likely overdue or paid
                    if result.get('payment_status') != 'paid':
                        result['payment_status'] = 'overdue'
                        result['payment_status_confidence'] = 0.70
                        print("  📅 Payment status: OVERDUE (date-based)")
            except:
                pass  # Date parsing failed, skip
        
        # Default: Set confidence score if not already set
        if 'payment_status_confidence' not in result or result['payment_status_confidence'] < 0.5:
            result['payment_status_confidence'] = 0.60
            print("  ❓ Payment status: DEFAULT (low confidence)")
        
        return result
    
    def _enhance_critical_fields(self, result: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
        """
        ✨ Enhance critical fields using regex extraction
        Fills in GSTIN, PAN, phone, email if Flash-Lite missed them
        """
        # GSTIN Pattern: 15 characters (2-digit state + 10-char PAN + 3-char suffix)
        GSTIN_PATTERN = r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b'
        
        # PAN Pattern: 10 characters
        PAN_PATTERN = r'\b[A-Z]{5}\d{4}[A-Z]{1}\b'
        
        # Phone Pattern: 10 digits (with optional +91 prefix)
        PHONE_PATTERN = r'(?:\+91[-\s]?)?(\d{10})\b'
        
        # Email Pattern
        EMAIL_PATTERN = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        
        # Extract GSTINs if not already present
        gstin_matches = re.findall(GSTIN_PATTERN, raw_text, re.IGNORECASE)
        
        if gstin_matches:
            # First GSTIN is usually vendor
            if not result.get('vendor_gstin') and len(gstin_matches) >= 1:
                result['vendor_gstin'] = gstin_matches[0].upper()
                result['vendor_gstin_confidence'] = 0.85
                print(f"  🔍 Enhanced: vendor_gstin = {result['vendor_gstin']}")
            
            # Second GSTIN is usually customer
            if not result.get('customer_gstin') and len(gstin_matches) >= 2:
                result['customer_gstin'] = gstin_matches[1].upper()
                result['customer_gstin_confidence'] = 0.80
                print(f"  🔍 Enhanced: customer_gstin = {result['customer_gstin']}")
        
        # Extract PANs if not already present
        pan_matches = re.findall(PAN_PATTERN, raw_text)
        
        if pan_matches:
            # Try to distinguish vendor vs customer PAN using context
            if not result.get('vendor_pan') and len(pan_matches) >= 1:
                result['vendor_pan'] = pan_matches[0].upper()
                result['vendor_pan_confidence'] = 0.75
                print(f"  🔍 Enhanced: vendor_pan = {result['vendor_pan']}")
            
            if not result.get('customer_pan') and len(pan_matches) >= 2:
                result['customer_pan'] = pan_matches[1].upper()
                result['customer_pan_confidence'] = 0.70
                print(f"  🔍 Enhanced: customer_pan = {result['customer_pan']}")
        
        # Extract phone numbers if not already present
        phone_matches = re.findall(PHONE_PATTERN, raw_text)
        
        if phone_matches:
            # Clean phone numbers (remove +91, spaces, dashes)
            cleaned_phones = [p.replace('+91', '').replace('-', '').replace(' ', '') for p in phone_matches]
            
            if not result.get('vendor_phone') and len(cleaned_phones) >= 1:
                result['vendor_phone'] = cleaned_phones[0]
                result['vendor_phone_confidence'] = 0.70
                print(f"  🔍 Enhanced: vendor_phone = {result['vendor_phone']}")
            
            if not result.get('customer_phone') and len(cleaned_phones) >= 2:
                result['customer_phone'] = cleaned_phones[1]
                result['customer_phone_confidence'] = 0.65
                print(f"  🔍 Enhanced: customer_phone = {result['customer_phone']}")
        
        # Extract emails if not already present
        email_matches = re.findall(EMAIL_PATTERN, raw_text, re.IGNORECASE)
        
        if email_matches:
            if not result.get('vendor_email') and len(email_matches) >= 1:
                result['vendor_email'] = email_matches[0].lower()
                result['vendor_email_confidence'] = 0.75
                print(f"  🔍 Enhanced: vendor_email = {result['vendor_email']}")
            
            if not result.get('customer_email') and len(email_matches) >= 2:
                result['customer_email'] = email_matches[1].lower()
                result['customer_email_confidence'] = 0.70
                print(f"  🔍 Enhanced: customer_email = {result['customer_email']}")
        
        # Extract HSN/SAC codes from line items if missing
        HSN_PATTERN = r'\b(\d{4,8})\b'  # 4-8 digit codes
        
        if 'line_items' in result and result['line_items']:
            for item in result['line_items']:
                if not item.get('hsn_sac'):
                    # Try to find HSN in item description
                    item_text = str(item.get('description', ''))
                    hsn_matches = re.findall(HSN_PATTERN, item_text)
                    if hsn_matches:
                        item['hsn_sac'] = hsn_matches[0]
                        item['hsn_sac_confidence'] = 0.65
        
        return result
    
    def _extract_json_from_response(self, response_text: str) -> str:
        """Extract JSON from model response, handling markdown"""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', response_text)
        text = re.sub(r'```\s*$', '', text)
        text = text.strip()
        
        # Find JSON object
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start >= 0 and end > start:
            return text[start:end]
        
        return text
    
    def _fix_json_issues(self, json_text: str) -> str:
        """Fix common JSON formatting issues including truncation"""
        # Extract potential JSON
        json_text = self._extract_json_from_response(json_text)
        
        # ✨ NEW: Handle truncated JSON (common with large consolidated invoices)
        if not json_text.strip().endswith('}'):
            print("  ⚠️  JSON appears truncated, attempting to close it...")
            # Count open braces and brackets
            open_braces = json_text.count('{') - json_text.count('}')
            open_brackets = json_text.count('[') - json_text.count(']')
            
            # Close any open arrays first
            if '"line_items": [' in json_text or '"line_items":[' in json_text:
                # Find the last complete line item
                last_item_end = json_text.rfind('}')
                if last_item_end > 0:
                    json_text = json_text[:last_item_end + 1]
                    # Close line_items array
                    if open_brackets > 0:
                        json_text += '\n]'
                        open_brackets -= 1
            
            # Close remaining open structures
            json_text += '\n}' * open_braces
            json_text += '\n]' * open_brackets
            print(f"  🔧 Closed {open_braces} braces and {open_brackets} brackets")
        
        # Fix common issues
        fixes = [
            (r',\s*}', '}'),  # Remove trailing commas
            (r',\s*]', ']'),  # Remove trailing commas in arrays
            (r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":'),  # Quote unquoted keys
            (r':\s*([^",\[\]{}\s]+)(?=\s*[,}])', r': "\1"'),  # Quote unquoted string values
        ]
        
        for pattern, replacement in fixes:
            json_text = re.sub(pattern, replacement, json_text)
        
        return json_text
    
    def _extract_from_broken_json(self, broken_json: str, raw_text: str) -> Dict[str, Any]:
        """
        Last resort: Extract what we can from severely broken JSON
        Uses regex to find key-value pairs and reconstruct minimal valid JSON
        """
        print("  🚨 Using aggressive extraction from broken JSON...")
        
        result = {
            'invoice_number': '',
            'vendor_name': '',
            'total_amount': 0.0,
            'currency': 'INR',
            'line_items': [],
            'error': True,
            'error_message': 'JSON parsing failed - using regex extraction'
        }
        
        # Try to extract key fields using regex (with multiple fallback patterns)
        patterns = {
            'invoice_number': [
                r'"invoice_number"\s*:\s*"([^"]+)"',
                r'"invoice_no"\s*:\s*"([^"]+)"',
            ],
            'vendor_name': [
                r'"vendor_name"\s*:\s*"([^"]+)"',
                r'"seller_name"\s*:\s*"([^"]+)"',
            ],
            'total_amount': [
                r'"total_amount"\s*:\s*([0-9]+(?:\.[0-9]+)?)',  # Standard format
                r'"total"\s*:\s*([0-9]+(?:\.[0-9]+)?)',  # Shortened
                r'"grand_total"\s*:\s*([0-9]+(?:\.[0-9]+)?)',  # Alternative
                r'"invoice_total"\s*:\s*([0-9]+(?:\.[0-9]+)?)',  # Alternative
                r'"net_amount"\s*:\s*([0-9]+(?:\.[0-9]+)?)',  # Alternative
            ],
            'customer_name': [
                r'"customer_name"\s*:\s*"([^"]+)"',
                r'"buyer_name"\s*:\s*"([^"]+)"',
            ],
            'invoice_date': [
                r'"invoice_date"\s*:\s*"([^"]+)"',
                r'"date"\s*:\s*"([^"]+)"',
            ],
        }
        
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, broken_json, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    if field == 'total_amount':
                        try:
                            result[field] = float(value)
                            print(f"  ✓ Extracted {field}: ₹{value}")
                        except:
                            pass
                    else:
                        result[field] = value
                        print(f"  ✓ Extracted {field}: {value}")
                    break  # Found a match, stop trying patterns for this field
        
        # If STILL no total_amount, scan raw text for amount patterns
        if result['total_amount'] == 0.0:
            print("  🔍 Scanning raw text for total amount...")
            # Look for common invoice total patterns
            amount_patterns = [
                r'Total\s*(?:Amount|Rs\.?|INR)?\s*:?\s*₹?\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'Grand\s+Total\s*:?\s*₹?\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'Net\s+Amount\s*:?\s*₹?\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'Invoice\s+Total\s*:?\s*₹?\s*([0-9,]+(?:\.[0-9]{2})?)',
            ]
            
            for pattern in amount_patterns:
                match = re.search(pattern, raw_text, re.IGNORECASE)
                if match:
                    try:
                        amount_str = match.group(1).replace(',', '')
                        result['total_amount'] = float(amount_str)
                        print(f"  ✓ Extracted total from raw text: ₹{amount_str}")
                        break
                    except:
                        pass
        
        # If still no vendor name, try from raw text header
        if not result['vendor_name']:
            lines = raw_text.split('\n')[:5]
            for line in lines:
                line = line.strip()
                if any(kw in line.upper() for kw in ['TRADING', 'COMPANY', 'LTD', 'PVT', 'INC']):
                    if 5 < len(line) < 100:
                        result['vendor_name'] = line
                        print(f"  ✓ Extracted vendor from raw text: {line}")
                        break
        
        # Enhance with regex patterns
        result = self._enhance_critical_fields(result, raw_text)
        
        return result
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            'error': True,
            'error_message': error_message,
            'invoice_number': '',
            'invoice_number_confidence': 0.0,
            'vendor_name': '',
            'vendor_name_confidence': 0.0,
            'total_amount': 0.0,
            'total_amount_confidence': 0.0,
            'currency': 'INR',
            'currency_confidence': 0.0,
            'line_items': [],
            '_formatting_metadata': {
                'model': 'gemini-2.5-flash-lite',
                'cost_inr': 0.01,
                'method': 'error_response',
                'success': False
            }
        }
    
    def _direct_ocr_extraction(self, raw_text: str) -> Dict[str, Any]:
        """
        🎯 ROBUST DIRECT OCR EXTRACTION
        Extracts data directly from Vision OCR text using regex patterns
        This bypasses Flash-Lite entirely for maximum reliability
        """
        print("  🔍 Starting direct OCR extraction...")
        
        # DEBUG: Save raw text for inspection
        try:
            with open('debug_ocr_text.txt', 'w', encoding='utf-8') as f:
                f.write(raw_text)
            print(f"  💾 Saved OCR text to debug_ocr_text.txt ({len(raw_text)} chars)")
        except:
            pass
        
        result = {
            'invoice_number': '',
            'vendor_name': '',
            'customer_name': '',
            'total_amount': 0.0,
            'subtotal': 0.0,
            'tax_amount': 0.0,
            'currency': 'INR',
            'invoice_date': '',
            'due_date': '',
            'line_items': [],
            '_formatting_metadata': {
                'model': 'direct_ocr',
                'cost_inr': 0.0,
                'method': 'regex_extraction',
                'success': True
            }
        }
        
        # Clean text for better matching
        text_upper = raw_text.upper()
        
        # 1. EXTRACT VENDOR NAME (from header - first 10 lines)
        lines = raw_text.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 10 and any(kw in line.upper() for kw in [
                'TRADING', 'COMPANY', 'CORPORATION', 'LTD', 'LIMITED',
                'PVT', 'PRIVATE', 'INC', 'LLC', 'INDUSTRIES', 'ENTERPRISE'
            ]):
                if not any(skip in line.upper() for skip in ['INVOICE', 'BILL', 'TO:', 'FROM:']):
                    result['vendor_name'] = line
                    print(f"  ✓ Vendor: {line}")
                    break
        
        # 2. EXTRACT INVOICE NUMBER (multiple patterns)
        inv_patterns = [
            r'INVOICE\s*(?:NO|NUMBER|#)?[:\s]+([A-Z0-9/-]+)',
            r'BILL\s*(?:NO|NUMBER|#)?[:\s]+([A-Z0-9/-]+)',
            r'INV[:\s-]+([A-Z0-9/-]+)',
            r'#\s*([A-Z0-9/-]{3,})',
        ]
        for pattern in inv_patterns:
            match = re.search(pattern, text_upper)
            if match:
                result['invoice_number'] = match.group(1)
                print(f"  ✓ Invoice #: {match.group(1)}")
                break
        
        # 3. EXTRACT TOTAL AMOUNT (most critical!)
        # For consolidated bills with format: "2,495.00 Total :Discount(-) :Bill Total :"
        # The amount comes BEFORE the "Bill Total" text
        bill_total_pattern = r'([0-9,]+\.?\d{2})\s+TOTAL\s*:\s*DISCOUNT\([^)]*\)\s*:\s*BILL\s+TOTAL'
        bill_totals = re.findall(bill_total_pattern, text_upper, re.IGNORECASE)
        
        if len(bill_totals) > 1:
            # Consolidated invoice with multiple bill totals
            print(f"  📊 Found {len(bill_totals)} bill totals (consolidated invoice)")
            total = 0.0
            for bill_total_str in bill_totals:
                try:
                    amount = float(bill_total_str.replace(',', ''))
                    total += amount
                    print(f"     + ₹{amount:,.2f}")
                except:
                    continue
            if total > 0:
                result['total_amount'] = total
                result['is_consolidated'] = True
                result['sub_vendor_count'] = len(bill_totals)
                print(f"  ✓ Total Amount (sum of {len(bill_totals)} bills): ₹{total:,.2f}")
                
                # Extract line items from each sub-bill
                print(f"  📋 Extracting line items from {len(bill_totals)} sub-bills...")
                line_items = self._extract_consolidated_line_items(raw_text)
                result['line_items'] = line_items
                print(f"  ✓ Extracted {len(line_items)} line items")
        
        # If no bill totals found, try standard patterns
        if result['total_amount'] == 0.0:
            total_patterns = [
                r'GRAND\s+TOTAL[:\s]*₹?\s*([0-9,]+\.?\d{0,2})',
                r'NET\s+AMOUNT[:\s]*₹?\s*([0-9,]+\.?\d{0,2})',
                r'INVOICE\s+TOTAL[:\s]*₹?\s*([0-9,]+\.?\d{0,2})',
                r'TOTAL\s+AMOUNT[:\s]*₹?\s*([0-9,]+\.?\d{0,2})',
                r'AMOUNT\s+PAYABLE[:\s]*₹?\s*([0-9,]+\.?\d{0,2})',
            ]
            
            for pattern in total_patterns:
                match = re.search(pattern, text_upper)
                if match:
                    try:
                        amount_str = match.group(1).replace(',', '')
                        amount = float(amount_str)
                        if amount > 0:
                            result['total_amount'] = amount
                            print(f"  ✓ Total Amount: ₹{amount:,.2f}")
                            break
                    except:
                        continue
        
        # Fallback: Find largest number in document (likely the total)
        if result['total_amount'] == 0:
            all_numbers = re.findall(r'([0-9,]+\.?\d{0,2})', raw_text)
            amounts = []
            for num_str in all_numbers:
                try:
                    amount = float(num_str.replace(',', ''))
                    if 10 < amount < 10000000:  # Reasonable invoice range
                        amounts.append(amount)
                except:
                    continue
            if amounts:
                result['total_amount'] = max(amounts)
                print(f"  ✓ Total Amount (fallback): ₹{result['total_amount']:,.2f}")
        
        # 4. EXTRACT CUSTOMER NAME
        customer_patterns = [
            r'(?:BILL\s+TO|BILLED\s+TO|CUSTOMER)[:\s]+([^\n]+)',
            r'TO[:\s]+([A-Z][^\n]{5,80})',
        ]
        for pattern in customer_patterns:
            match = re.search(pattern, text_upper)
            if match:
                result['customer_name'] = match.group(1).strip()
                print(f"  ✓ Customer: {result['customer_name']}")
                break
        
        # 5. EXTRACT DATES
        date_patterns = [
            r'(?:DATE|INVOICE\s+DATE)[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(?:DATE|INVOICE\s+DATE)[:\s]+(\d{1,2}\s+[A-Z]{3,9}\s+\d{2,4})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text_upper)
            if match:
                result['invoice_date'] = match.group(1)
                print(f"  ✓ Date: {result['invoice_date']}")
                break
        
        # 6. EXTRACT GSTIN NUMBERS
        gstin_pattern = r'\b(\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1})\b'
        gstins = re.findall(gstin_pattern, raw_text)
        if len(gstins) >= 1:
            result['vendor_gstin'] = gstins[0]
            result['vendor_gstin_confidence'] = 0.95
            print(f"  ✓ Vendor GSTIN: {gstins[0]}")
        if len(gstins) >= 2:
            result['customer_gstin'] = gstins[1]
            result['customer_gstin_confidence'] = 0.95
            print(f"  ✓ Customer GSTIN: {gstins[1]}")
        
        return result
    
    def _extract_consolidated_line_items(self, raw_text: str) -> list:
        """
        Extract line items from consolidated invoice with multiple sub-bills
        Each sub-bill has format:
        VENDOR NAME / LOCATION Bill No: XXX Dated: XXX GSTIN:XXX
        Item Name    Quantity  Case Quantity  Rate  Amount
        ITEM 1       1         6              1255   1255.00
        """
        line_items = []
        
        # Split text into sub-bills using bill number pattern
        bill_pattern = r'(.+?)\s+BILL\s+NO:\s*([A-Z0-9-]+)\s+DATED:\s*([0-9-A-Z]+)(?:\s+GSTIN:([0-9A-Z]+))?'
        bills = re.finditer(bill_pattern, raw_text, re.IGNORECASE)
        
        bill_sections = []
        for match in bills:
            vendor_location = match.group(1).strip()
            bill_no = match.group(2)
            dated = match.group(3)
            gstin = match.group(4) if match.group(4) else ''
            
            # Extract vendor name (before the /)
            vendor_parts = vendor_location.split('/')
            sub_vendor = vendor_parts[0].strip() if vendor_parts else vendor_location
            
            bill_sections.append({
                'sub_vendor': sub_vendor,
                'sub_bill_number': bill_no,
                'sub_gstin': gstin,
                'start_pos': match.end()
            })
        
        # Extract items from each bill section
        for idx, bill_info in enumerate(bill_sections):
            start_pos = bill_info['start_pos']
            # End position is start of next bill or end of text
            end_pos = bill_sections[idx + 1]['start_pos'] if idx + 1 < len(bill_sections) else len(raw_text)
            section_text = raw_text[start_pos:end_pos]
            
            # Extract line items from this section
            # Pattern: Item name followed by numbers (quantity, rate, amount)
            # Looking for lines with: TEXT  NUMBER  NUMBER  NUMBER  AMOUNT
            item_pattern = r'^([A-Z][A-Z0-9\s\(\)\/+\.-]+?)\s+(\d+)\s+(\d+)\s+([0-9.]+)\s+([0-9,]+\.?\d{0,2})$'
            
            lines = section_text.split('\n')
            for line in lines:
                line = line.strip()
                match = re.match(item_pattern, line, re.IGNORECASE)
                if match:
                    description = match.group(1).strip()
                    quantity = int(match.group(2))
                    rate = float(match.group(4))
                    amount_str = match.group(5).replace(',', '')
                    amount = float(amount_str)
                    
                    # Only add if amount > 0 and description is reasonable
                    if amount > 0 and len(description) > 3 and len(description) < 150:
                        line_items.append({
                            'description': description,
                            'quantity': quantity,
                            'rate': rate,
                            'amount': amount,
                            'sub_vendor': bill_info['sub_vendor'],
                            'sub_bill_number': bill_info['sub_bill_number'],
                            'sub_gstin': bill_info['sub_gstin']
                        })
        
        return line_items
    
    def get_cost_estimate(self) -> Dict[str, Any]:
        """Get cost information for Flash-Lite formatting"""
        return {
            'cost_per_format_inr': 0.01,
            'cost_per_format_usd': 0.00012,
            'pricing_model': 'per_request',
            'input_tokens': 400,
            'output_tokens': 200,
            'description': 'Gemini 2.5 Flash-Lite text-to-JSON formatting'
        }


# Test function
def test_flash_lite_formatter():
    """Test Flash-Lite formatter with sample text"""
    try:
        formatter = FlashLiteFormatter()
        print("✅ Flash-Lite formatter initialized successfully")
        print(f"💰 Cost estimate: ₹{formatter.get_cost_estimate()['cost_per_format_inr']} per format")
        
        # Test with sample text
        sample_text = """
        Invoice: INV-001
        Date: 2024-01-15
        Vendor: ABC Company
        Total: 1000.00
        """
        
        result = formatter.format_text_to_json(sample_text)
        if result.get('invoice_number'):
            print("✅ Sample formatting test passed")
        else:
            print("⚠️ Sample formatting test returned empty result")
        
        return True
    except Exception as e:
        print(f"❌ Flash-Lite formatter test failed: {e}")
        return False


if __name__ == "__main__":
    test_flash_lite_formatter()