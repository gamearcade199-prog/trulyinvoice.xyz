"""
🔍 VISION OCR + FLASH-LITE FORMATTER
Strict Vision API OCR + Gemini 2.5 Flash-Lite JSON formatting
No Gemini fallback - requires Vision API to be available
"""

import os
import time
from typing import Dict, Any, Optional

# Require Vision API - no fallback allowed
from .vision_extractor import VisionExtractor
from .flash_lite_formatter import FlashLiteFormatter


class VisionOCR_FlashLite_Extractor:
    """Strict Vision API OCR + Flash-Lite JSON formatter (no Gemini fallback)"""

    def __init__(self):
        """Initialize with strict Vision API requirement"""
        try:
            self.vision_extractor = VisionExtractor()
            print("✅ VISION API INITIALIZED - OCR extraction ready")
        except Exception as e:
            raise RuntimeError(f"❌ VISION API REQUIRED but failed to initialize: {e}. Please ensure Vision API is properly configured.")

        try:
            self.flash_lite_formatter = FlashLiteFormatter()
            print("✅ GEMINI 2.5 FLASH-LITE INITIALIZED - JSON formatting ready")
        except Exception as e:
            raise RuntimeError(f"❌ FLASH-LITE REQUIRED but failed to initialize: {e}")

        print("🚀 VISION OCR + FLASH-LITE SYSTEM READY")
        print("💰 Cost: ₹0.12 (Vision) + ₹0.01 (Flash-Lite) = ₹0.13 per invoice")

    def extract_invoice_data(self, image_data: bytes, image_filename: str = "unknown") -> Dict[str, Any]:
        """
        Strict Vision OCR + Flash-Lite formatting pipeline

        Args:
            image_data: Raw image bytes
            image_filename: Original filename for logging

        Returns:
            Structured invoice data with confidence scores
        """
        start_time = time.time()

        print(f"🔍 Processing: {image_filename}")
        print("📸 VISION OCR + ⚡ FLASH-LITE FORMATTING")
        print("=" * 50)

        try:
            # Step 1: Extract raw text using Vision API OCR (₹0.12)
            print("📸 Step 1: Vision API OCR text extraction...")
            vision_result = self.vision_extractor.extract_text_from_image(image_data)

            if not vision_result['success']:
                error_msg = vision_result.get('error', 'Vision API extraction failed')
                print(f"❌ Vision OCR failed: {error_msg}")
                return self._create_error_response(error_msg, image_filename)

            extracted_text = vision_result['extracted_text']
            vision_confidence = vision_result['confidence']

            print(f"✅ Vision OCR: {len(extracted_text)} characters extracted")
            print(f"📊 Vision confidence: {vision_confidence:.1%}")

            # Step 2: Format text to JSON using Flash-Lite (₹0.01)
            print("⚡ Step 2: Flash-Lite JSON formatting...")
            formatted_result = self.flash_lite_formatter.format_text_to_json(extracted_text)

            if formatted_result.get('error'):
                error_msg = f"Flash-Lite formatting failed: {formatted_result.get('error_message', 'Unknown error')}"
                print(f"❌ {error_msg}")
                return self._create_error_response(error_msg, image_filename, extracted_text)

            # Step 3: Combine results and add metadata
            processing_time = time.time() - start_time

            # Add extraction metadata
            formatted_result['_extraction_metadata'] = {
                'method': 'vision_ocr_flash_lite',
                'ocr_model': 'google_vision_api',
                'formatter_model': 'gemini_2.5_flash_lite',
                'vision_api_cost_inr': 0.12,
                'flash_lite_cost_inr': 0.01,
                'total_cost_inr': 0.13,
                'processing_time_seconds': round(processing_time, 2),
                'vision_confidence': vision_confidence,
                'text_length': len(extracted_text),
                'filename': image_filename,
                'success': True
            }

            # Calculate overall quality score
            overall_confidence = self._calculate_overall_confidence(formatted_result, vision_confidence)
            quality_grade = self._get_quality_grade(overall_confidence)

            print("=" * 50)
            print("📊 EXTRACTION QUALITY REPORT")
            print("=" * 50)
            print(f"🎯 Overall Confidence: {overall_confidence:.1%}")
            print(f"🏅 Quality Grade: {quality_grade}")
            print(f"⚡ Processing Time: {processing_time:.1f} seconds")
            print(f"💰 Total Cost: ₹0.13")

            # Count extracted fields
            field_count = self._count_extracted_fields(formatted_result)
            print(f"📋 Total fields extracted: {field_count}")

            # Count line items
            line_items = formatted_result.get('line_items', [])
            print(f"📊 Line items extracted: {len(line_items)}")
            print()

            # Create summary
            vendor_name = formatted_result.get('vendor_name', 'Unknown')
            total_amount = formatted_result.get('total_amount', 0)
            currency = formatted_result.get('currency', 'INR')

            print(f"✅ Extracted: {vendor_name} - {currency} {total_amount:,.2f}")
            print("=" * 50)

            return formatted_result

        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Vision OCR + Flash-Lite extraction error: {str(e)}"
            print(f"❌ {error_msg}")
            return self._create_error_response(error_msg, image_filename, processing_time=processing_time)

    def _calculate_overall_confidence(self, formatted_data: Dict[str, Any], vision_confidence: float) -> float:
        """Calculate overall confidence score"""
        try:
            # Get confidence scores from formatted data
            confidence_fields = [k for k in formatted_data.keys() if k.endswith('_confidence')]

            if confidence_fields:
                confidence_values = [formatted_data[field] for field in confidence_fields if isinstance(formatted_data[field], (int, float))]
                avg_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0.5
            else:
                avg_confidence = 0.5

            # Combine with vision confidence (weighted average)
            overall = (vision_confidence * 0.4) + (avg_confidence * 0.6)
            return max(0.0, min(1.0, overall))

        except:
            return 0.5

    def _get_quality_grade(self, confidence: float) -> str:
        """Get quality grade based on confidence"""
        if confidence >= 0.95:
            return "EXCELLENT"
        elif confidence >= 0.85:
            return "VERY_GOOD"
        elif confidence >= 0.75:
            return "GOOD"
        elif confidence >= 0.60:
            return "FAIR"
        else:
            return "NEEDS_REVIEW"

    def _count_extracted_fields(self, data: Dict[str, Any]) -> int:
        """Count non-empty extracted fields"""
        count = 0
        exclude_keys = {'_extraction_metadata', '_formatting_metadata', 'line_items', 'error', 'error_message'}

        for key, value in data.items():
            if key in exclude_keys or key.endswith('_confidence'):
                continue

            if value and value != '' and value != 0:
                count += 1

        return count

    def _create_error_response(self, error: str, filename: str, raw_text: str = '', processing_time: float = 0) -> Dict[str, Any]:
        """Create error response"""
        return {
            'error': True,
            'error_message': error,
            'invoice_number': '',
            'invoice_number_confidence': 0.0,
            'vendor_name': filename.replace('.jpg', '').replace('.png', '').replace('.pdf', ''),
            'vendor_name_confidence': 0.1,
            'total_amount': 0.0,
            'total_amount_confidence': 0.0,
            'currency': 'INR',
            'currency_confidence': 1.0,
            'line_items': [],
            '_extraction_metadata': {
                'method': 'vision_ocr_flash_lite_error',
                'ocr_model': 'google_vision_api',
                'formatter_model': 'gemini_2.5_flash_lite',
                'total_cost_inr': 0.13,
                'processing_time_seconds': processing_time,
                'success': False,
                'error': error,
                'raw_text_length': len(raw_text)
            }
        }

    def get_cost_estimate(self) -> Dict[str, Any]:
        """Get cost estimate"""
        return {
            'vision_ocr_cost_inr': 0.12,
            'flash_lite_formatting_cost_inr': 0.01,
            'total_cost_inr': 0.13,
            'ocr_model': 'Google Vision API',
            'formatter_model': 'Gemini 2.5 Flash-Lite',
            'description': 'Vision OCR + Flash-Lite JSON formatting'
        }