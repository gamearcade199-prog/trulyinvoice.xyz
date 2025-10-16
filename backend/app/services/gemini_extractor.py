"""
🛡️ BULLETPROOF GEMINI 2.5 FLASH EXTRACTOR
Handles 30+ potential issues, covers all database fields
"""

import os
import json
import base64
import hashlib
import re
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from typing import Dict, Any, Optional, Union
import google.generativeai as genai


class GeminiExtractor:
    def __init__(self):
        """Initialize bulletproof Gemini 2.5 Flash extractor"""
        # Issue #1: Missing API key
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_AI_API_KEY environment variable not set")
        
        # Issue #2: Invalid API key format
        if not api_key.startswith('AIza'):
            raise ValueError("Invalid Google AI API key format")
        
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Failed to configure Gemini API: {e}")
        
        # Issue #3: Wrong model name
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        
        # Issue #4: Model initialization failure
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            # Fallback to experimental if production fails
            try:
                self.model_name = 'gemini-2.0-flash-exp'
                self.model = genai.GenerativeModel(self.model_name)
                print(f"⚠️ Fallback to experimental model: {self.model_name}")
            except Exception as fallback_e:
                raise ValueError(f"Failed to initialize any Gemini model: {e}, {fallback_e}")
        
        # Issue #5: Single attempt for maximum speed (no retries)
        self.timeout_seconds = 10  # Fast response required
        self.max_retries = 0  # NO RETRIES - Single attempt only
        
        print(f"✅ BULLETPROOF GEMINI {self.model_name} extraction ENABLED - 95% accuracy target")

    def extract_from_text(self, text: str, original_filename: str = "unknown.txt") -> Optional[Dict[str, Any]]:
        """🛡️ BULLETPROOF text extraction"""
        # Issue #6: Empty or None text
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            print("  ❌ Empty or invalid text provided")
            return None
        
        # Issue #7: Text too long (token limit)
        if len(text) > 500000:  # ~125k tokens
            print(f"  ⚠️ Text too long ({len(text)} chars), truncating...")
            text = text[:500000]
        
        print(f"\n{'='*60}")
        print(f"⚡ BULLETPROOF GEMINI EXTRACTION")
        print(f"{'='*60}")
        
        result = self._extract_invoice_data(text, is_vision=False)
        return self._finalize_result(result, original_filename)

    def extract_from_image(self, image_path: str = None, image_base64: str = None, 
                          mime_type: str = "image/jpeg", original_filename: str = "unknown.jpg") -> Optional[Dict[str, Any]]:
        """🛡️ BULLETPROOF image extraction"""
        print(f"\n{'='*60}")
        print(f"⚡ BULLETPROOF GEMINI EXTRACTION")
        print(f"{'='*60}")
        
        try:
            # Issue #8: Both image_path and image_base64 provided
            if image_path and image_base64:
                print("  ⚠️ Both image_path and image_base64 provided, using image_base64")
            
            # Issue #9: File path handling
            if image_path:
                if not os.path.exists(image_path):
                    print(f"  ❌ Image file not found: {image_path}")
                    return None
                
                try:
                    with open(image_path, 'rb') as f:
                        image_data = f.read()
                        # Issue #10: Empty file
                        if len(image_data) == 0:
                            print("  ❌ Image file is empty")
                            return None
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                except Exception as e:
                    print(f"  ❌ Failed to read image file: {e}")
                    return None
            
            # Issue #11: No image data provided
            if not image_base64:
                print("  ❌ No image data provided")
                return None
            
            # Issue #12: Invalid image_base64 type
            if not isinstance(image_base64, str):
                print(f"  ❌ Invalid image_base64 type: {type(image_base64)}")
                return None
            
            # Issue #13: Invalid base64 format
            try:
                decoded_data = base64.b64decode(image_base64)
                if len(decoded_data) == 0:
                    print("  ❌ Base64 decodes to empty data")
                    return None
            except Exception as e:
                print(f"  ❌ Invalid base64 data: {e}")
                return None
            
            # Issue #14: Image too large (20MB limit)
            if len(decoded_data) > 20 * 1024 * 1024:
                print(f"  ❌ Image too large: {len(decoded_data)} bytes (max 20MB)")
                return None
            
            # Issue #15: Invalid MIME type
            valid_mimes = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
            if mime_type not in valid_mimes:
                print(f"  ⚠️ Invalid MIME type {mime_type}, defaulting to image/jpeg")
                mime_type = 'image/jpeg'
            
            result = self._extract_invoice_data(None, is_vision=True, image_base64=image_base64, mime_type=mime_type)
            return self._finalize_result(result, original_filename, extraction_type='vision_ocr')
            
        except Exception as e:
            print(f"  ❌ Image processing error: {e}")
            return None

    def _extract_invoice_data(self, text: str = None, is_vision: bool = False, 
                             image_base64: str = None, mime_type: str = None) -> Optional[Dict[str, Any]]:
        """🛡️ BULLETPROOF single extraction with comprehensive field support"""
        
        # Issue #16: Speed-optimized prompt for 5-10 second processing
        prompt = """🚀 FAST INDIAN INVOICE EXTRACTION - 99% ACCURACY IN 5 SECONDS

TASK: Extract ALL invoice data with confidence scores (0.0-1.0) in ONE SHOT.

RULES: 
1. Extract ONLY fields that exist
2. Return ONLY valid JSON 
3. Include confidence for each field
4. Remove currency symbols (₹,$,€)
5. Dates as YYYY-MM-DD

CORE FIELDS:
- invoice_number, invoice_number_confidence
- invoice_date, invoice_date_confidence  
- vendor_name, vendor_name_confidence
- total_amount, total_amount_confidence
- currency, currency_confidence

OPTIONAL FIELDS (if visible):
VENDOR: vendor_gstin, vendor_pan, vendor_email, vendor_phone, vendor_address, vendor_state, vendor_pincode
CUSTOMER: customer_name, customer_gstin, customer_address, customer_state, customer_phone  
FINANCIAL: subtotal, taxable_amount, discount, shipping_charges, other_charges, roundoff
GST: cgst, sgst, igst, ugst, cess, total_gst, hsn_code, sac_code, place_of_supply
BANKING: bank_name, account_number, ifsc_code, swift_code
PAYMENT: payment_status, payment_method, payment_terms
DATES: due_date, po_number, po_date
TAXES: vat, service_tax, tds_amount, tcs_amount
TRADE: invoice_type, supply_type, reverse_charge
IMPORT: bill_of_entry, port_code

INDUSTRY SPECIFIC (extract if present):
HOTEL: arrival_date, departure_date, room_number, guest_count, booking_reference, meal_plan
RETAIL: order_id, tracking_number, shipping_method, delivery_date, coupon_code, discount_percentage
MANUFACTURING: purchase_order, batch_number, quality_certificate, warranty_period, manufacturing_date, expiry_date
MEDICAL: patient_id, doctor_name, medical_license, insurance_claim, treatment_date, prescription_number
LOGISTICS: vehicle_number, driver_name, origin_location, destination_location, distance_km, fuel_surcharge
SERVICES: project_name, consultant_name, hourly_rate, hours_worked, project_phase
REAL_ESTATE: property_address, property_type, square_footage, lease_term, security_deposit
EDUCATION: student_id, course_name, academic_year, semester, instructor_name
UTILITIES: meter_reading_start, meter_reading_end, units_consumed, rate_per_unit, connection_id
SUBSCRIPTION: subscription_type, billing_cycle, next_billing_date, auto_renewal, plan_features

LINE ITEMS: Extract ALL table rows as:
{"description": "item", "quantity": 1, "rate": 100, "amount": 100, "confidence": 0.95}

OUTPUT (JSON ONLY):
{
  "invoice_number": "INV-001", "invoice_number_confidence": 0.98,
  "vendor_name": "Company", "vendor_name_confidence": 0.95,
  "total_amount": 40000, "total_amount_confidence": 1.0,
  "currency": "INR", "currency_confidence": 1.0,
  "line_items": [{"description": "Service", "quantity": 1, "rate": 40000, "amount": 40000, "confidence": 0.95}],
  "payment_status": "pending", "payment_status_confidence": 1.0
}

⚡ BE FAST & ACCURATE!

""" + ("Invoice text:\n" + text if text else "Analyze the invoice image:")

        for attempt in range(self.max_retries + 1):
            try:
                print(f"🔥 Extraction attempt {attempt + 1}/{self.max_retries + 1}...")
                
                # Issue #17: API call failure
                if is_vision:
                    # Issue #18: Vision API specific errors
                    response = self.model.generate_content([
                        prompt,
                        {
                            "mime_type": mime_type,
                            "data": image_base64
                        }
                    ])
                else:
                    # Issue #19: Text API specific errors
                    response = self.model.generate_content(prompt)
                
                # Issue #20: Empty response
                if not response:
                    print(f"  ❌ No response from Gemini (attempt {attempt + 1})")
                    continue
                
                # Issue #21: Response without text
                if not hasattr(response, 'text') or not response.text:
                    print(f"  ❌ Response has no text (attempt {attempt + 1})")
                    continue
                
                # Issue #22: API safety filters
                if hasattr(response, 'prompt_feedback'):
                    if response.prompt_feedback and hasattr(response.prompt_feedback, 'block_reason'):
                        print(f"  ❌ Content blocked: {response.prompt_feedback.block_reason}")
                        return None
                
                # Issue #23: JSON parsing with multiple formats
                result_text = response.text.strip()
                
                # Remove markdown formatting
                if result_text.startswith('```json'):
                    result_text = result_text[7:]
                elif result_text.startswith('```'):
                    result_text = result_text[3:]
                
                if result_text.endswith('```'):
                    result_text = result_text[:-3]
                
                # Remove extra whitespace
                result_text = result_text.strip()
                
                # Issue #24: Invalid JSON structure
                if not result_text.startswith('{') or not result_text.endswith('}'):
                    print(f"  ❌ Invalid JSON format (attempt {attempt + 1})")
                    continue
                
                # Issue #25: JSON parsing errors
                try:
                    result = json.loads(result_text)
                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON parsing error: {e} (attempt {attempt + 1})")
                    if attempt < self.max_retries:
                        continue
                    return None
                
                # Issue #26: Empty result
                if not result or not isinstance(result, dict):
                    print(f"  ❌ Empty or invalid result (attempt {attempt + 1})")
                    continue
                
                # Issue #27: Comprehensive validation and fixing
                result = self._bulletproof_validate_fix(result)
                
                print(f"   ✅ Extracted {len([k for k in result.keys() if not k.endswith('_confidence')])} fields")
                return result
                
            except Exception as e:
                print(f"  ❌ Extraction error: {e} (attempt {attempt + 1})")
                if attempt < self.max_retries:
                    continue
                return None
        
        print("  ❌ All extraction attempts failed")
        return None

    def _bulletproof_validate_fix(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """🛡️ Comprehensive validation and auto-fix for all issues"""
        
        # Issue #28: Data type conversions and validations
        
        # Fix numeric fields
        numeric_fields = [
            'total_amount', 'subtotal', 'taxable_amount', 'cgst', 'sgst', 'igst', 'ugst', 'cess',
            'total_gst', 'vat', 'service_tax', 'tds_amount', 'tds_percentage', 'tcs_amount',
            'discount', 'discount_percentage', 'shipping_charges', 'packing_charges',
            'handling_charges', 'insurance_charges', 'other_charges', 'roundoff'
        ]
        
        for field in numeric_fields:
            if field in result:
                result[field] = self._safe_convert_to_number(result[field])
        
        # Fix date fields
        date_fields = ['invoice_date', 'due_date', 'po_date', 'bill_of_entry_date']
        for field in date_fields:
            if field in result:
                result[field] = self._safe_convert_to_date(result[field])
        
        # Fix GSTIN format
        gstin_fields = ['vendor_gstin', 'customer_gstin']
        for field in gstin_fields:
            if field in result:
                result[field] = self._fix_gstin_format(result[field])
                # Lower confidence if invalid
                conf_field = f"{field}_confidence"
                if conf_field in result and len(str(result[field])) != 15:
                    result[conf_field] = min(0.7, result.get(conf_field, 0.8))
        
        # Fix PAN format
        if 'vendor_pan' in result:
            result['vendor_pan'] = self._fix_pan_format(result['vendor_pan'])
        
        # Fix confidence scores
        for key, value in result.items():
            if key.endswith('_confidence'):
                result[key] = self._safe_convert_confidence(value)
        
        # Fix line items
        if 'line_items' in result and isinstance(result['line_items'], list):
            result['line_items'] = self._fix_line_items(result['line_items'])
        
        # Ensure required defaults
        if 'payment_status' not in result:
            result['payment_status'] = 'unpaid'
            result['payment_status_confidence'] = 1.0
        else:
            # Normalize payment status to avoid constraint violations
            # VALID VALUES ONLY: paid, unpaid, partial, overdue
            status = str(result['payment_status']).lower()
            if status in ['paid', 'complete', 'completed', 'success', 'successful']:
                result['payment_status'] = 'paid'
            elif status in ['overdue', 'late', 'past_due']:
                result['payment_status'] = 'overdue'
            elif status in ['partial', 'partially_paid', 'part paid']:
                result['payment_status'] = 'partial'
            elif status in ['pending', 'unpaid', 'due', 'outstanding', 'cancelled', 'canceled', 'void', 'refunded', 'returned']:
                # Map all other statuses to unpaid (safe default)
                result['payment_status'] = 'unpaid'
            else:
                result['payment_status'] = 'unpaid'  # Safe default
        
        if 'currency' not in result and 'total_amount' in result:
            result['currency'] = 'INR'  # Default for Indian invoices
            result['currency_confidence'] = 0.9
        
        # Issue #29: Remove invalid/empty fields
        result = self._remove_invalid_fields(result)
        
        return result

    def _safe_convert_to_number(self, value: Any) -> Optional[float]:
        """Safely convert value to number"""
        if value is None or value == '':
            return None
        
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove currency symbols and commas
            cleaned = re.sub(r'[₹$€£,\s]', '', value)
            try:
                return float(cleaned)
            except (ValueError, TypeError):
                return None
        
        return None

    def _safe_convert_to_date(self, value: Any) -> Optional[str]:
        """Safely convert value to YYYY-MM-DD format"""
        if not value:
            return None
        
        if isinstance(value, date):
            return value.isoformat()
        
        if isinstance(value, str):
            # Try different date formats
            formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%m/%d/%Y']
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(value, fmt).date()
                    return parsed_date.isoformat()
                except ValueError:
                    continue
        
        return None

    def _fix_gstin_format(self, value: Any) -> Optional[str]:
        """Fix GSTIN format to 15 alphanumeric characters"""
        if not value:
            return None
        
        gstin = str(value).upper().replace(' ', '').replace('-', '')
        if len(gstin) == 15 and gstin.isalnum():
            return gstin
        
        return value  # Return original if can't fix

    def _fix_pan_format(self, value: Any) -> Optional[str]:
        """Fix PAN format to 10 characters"""
        if not value:
            return None
        
        pan = str(value).upper().replace(' ', '').replace('-', '')
        if len(pan) == 10 and pan[:5].isalpha() and pan[5:9].isdigit() and pan[9].isalpha():
            return pan
        
        return value  # Return original if can't fix

    def _safe_convert_confidence(self, value: Any) -> float:
        """Safely convert confidence to float between 0.0 and 1.0"""
        if isinstance(value, (int, float)):
            return max(0.0, min(1.0, float(value)))
        
        if isinstance(value, str):
            try:
                conf = float(value)
                return max(0.0, min(1.0, conf))
            except (ValueError, TypeError):
                return 0.8  # Default confidence
        
        return 0.8  # Default confidence

    def _fix_line_items(self, line_items: list) -> list:
        """Fix line items structure and data types"""
        fixed_items = []
        
        for item in line_items:
            if not isinstance(item, dict):
                continue
            
            fixed_item = {}
            
            # Required fields
            fixed_item['description'] = str(item.get('description', ''))
            fixed_item['quantity'] = self._safe_convert_to_number(item.get('quantity', 1)) or 1
            fixed_item['rate'] = self._safe_convert_to_number(item.get('rate', 0)) or 0
            fixed_item['amount'] = self._safe_convert_to_number(item.get('amount', 0)) or 0
            fixed_item['confidence'] = self._safe_convert_confidence(item.get('confidence', 0.8))
            
            # Optional fields
            if 'hsn_sac' in item:
                fixed_item['hsn_sac'] = str(item['hsn_sac'])
            if 'unit' in item:
                fixed_item['unit'] = str(item['unit'])
            if 'discount' in item:
                fixed_item['discount'] = self._safe_convert_to_number(item['discount'])
            
            fixed_items.append(fixed_item)
        
        return fixed_items

    def _remove_invalid_fields(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Remove fields with invalid or empty values, and unknown fields"""
        # Known database fields to prevent column errors
        known_fields = {
            'invoice_number', 'invoice_date', 'vendor_name', 'total_amount', 'currency',
            'vendor_gstin', 'vendor_pan', 'vendor_email', 'vendor_phone', 'vendor_address', 
            'vendor_state', 'vendor_pincode', 'customer_name', 'customer_gstin', 
            'customer_address', 'customer_state', 'customer_phone', 'subtotal',
            'taxable_amount', 'discount', 'shipping_charges', 'other_charges', 'roundoff',
            'cgst', 'sgst', 'igst', 'ugst', 'cess', 'total_gst', 'hsn_code', 'sac_code',
            'place_of_supply', 'bank_name', 'account_number', 'ifsc_code', 'swift_code',
            'payment_status', 'payment_method', 'payment_terms', 'due_date', 'po_number',
            'po_date', 'vat', 'service_tax', 'tds_amount', 'tcs_amount', 'invoice_type',
            'supply_type', 'reverse_charge', 'bill_of_entry', 'port_code', 'line_items',
            '_extraction_hash', '_extraction_metadata'
        }
        
        cleaned_result = {}
        
        for key, value in result.items():
            # Keep all confidence fields
            if key.endswith('_confidence'):
                cleaned_result[key] = value
                continue
            
            # Only keep known database fields
            if key not in known_fields:
                print(f"   ⚠️ Skipping unknown field: {key}")
                continue
            
            # Keep valid non-empty values
            if value is not None and value != '' and value != []:
                cleaned_result[key] = value
        
        return cleaned_result

    def _finalize_result(self, result: Optional[Dict[str, Any]], original_filename: str, extraction_type: str = 'text') -> Optional[Dict[str, Any]]:
        """Add metadata and generate quality report"""
        # Issue #30: Null result handling
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
        """Print comprehensive quality report"""
        metadata = result.get('_extraction_metadata', {})
        confidence = metadata.get('overall_confidence', 0)
        grade = metadata.get('quality_grade', 'UNKNOWN')
        
        print(f"\n{'='*60}")
        print(f"📊 BULLETPROOF GEMINI QUALITY REPORT")
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