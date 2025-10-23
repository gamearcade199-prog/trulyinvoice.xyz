"""
🔍 GOOGLE VISION API EXTRACTOR
Ultra-fast text extraction from invoice images at ₹0.12 per invoice
"""

import os
import base64
import json
from typing import Dict, Any, Optional

# Google Cloud Vision API (optional - will fall back to Gemini if not available)
try:
    from google.cloud import vision
    import google.auth
    from google.oauth2 import service_account
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False


class VisionExtractor:
    def __init__(self):
        """Initialize Google Vision API client"""
        if not VISION_AVAILABLE:
            raise ImportError("google-cloud-vision library not installed. Will use Gemini-only fallback.")
        
        # Use GOOGLE_VISION_API_KEY or fall back to GOOGLE_AI_API_KEY
        api_key = os.getenv('GOOGLE_VISION_API_KEY') or os.getenv('GOOGLE_AI_API_KEY') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_VISION_API_KEY, GOOGLE_AI_API_KEY, or GEMINI_API_KEY environment variable not set")
        
        # Initialize Vision client
        # Note: Vision API can use the same API key through REST API
        self.api_key = api_key
        self.vision_url = "https://vision.googleapis.com/v1/images:annotate"
        
    def extract_text_from_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract raw text from invoice image using Vision API
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dict containing extracted text and metadata
        """
        try:
            import requests
            
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare Vision API request
            request_data = {
                "requests": [
                    {
                        "image": {
                            "content": image_base64
                        },
                        "features": [
                            {
                                "type": "DOCUMENT_TEXT_DETECTION",
                                "maxResults": 1
                            }
                        ]
                    }
                ]
            }
            
            # Make API call
            response = requests.post(
                f"{self.vision_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json=request_data,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Vision API error: {response.status_code} - {response.text}")
            
            result = response.json()
            
            # Extract text from response
            if 'responses' in result and result['responses']:
                annotations = result['responses'][0]
                
                if 'fullTextAnnotation' in annotations:
                    extracted_text = annotations['fullTextAnnotation']['text']
                    
                    # Get bounding box information for better parsing
                    text_blocks = []
                    if 'textAnnotations' in annotations:
                        for annotation in annotations['textAnnotations'][1:]:  # Skip first (full text)
                            text_blocks.append({
                                'text': annotation['description'],
                                'bounds': annotation.get('boundingPoly', {})
                            })
                    
                    return {
                        'success': True,
                        'extracted_text': extracted_text,
                        'text_blocks': text_blocks,
                        'confidence': self._calculate_confidence(annotations),
                        'method': 'google_vision_api',
                        'cost_inr': 0.12  # Track cost
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No text detected in image',
                        'extracted_text': '',
                        'text_blocks': [],
                        'confidence': 0.0
                    }
            else:
                return {
                    'success': False,
                    'error': 'Invalid Vision API response',
                    'extracted_text': '',
                    'text_blocks': [],
                    'confidence': 0.0
                }
                
        except Exception as e:
            print(f"❌ Vision API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'extracted_text': '',
                'text_blocks': [],
                'confidence': 0.0
            }
    
    def _calculate_confidence(self, annotations: Dict) -> float:
        """Calculate overall confidence score from Vision API response"""
        try:
            if 'textAnnotations' in annotations and annotations['textAnnotations']:
                # Vision API doesn't provide confidence scores in the same way
                # We'll use the presence and quality of text detection as proxy
                text_length = len(annotations.get('fullTextAnnotation', {}).get('text', ''))
                num_words = len(annotations.get('fullTextAnnotation', {}).get('text', '').split())
                
                # Simple heuristic: longer text with more words = higher confidence
                if text_length > 100 and num_words > 10:
                    return 0.95
                elif text_length > 50 and num_words > 5:
                    return 0.85
                elif text_length > 20:
                    return 0.75
                else:
                    return 0.60
            return 0.50
        except:
            return 0.50
    
    def get_cost_estimate(self) -> Dict[str, Any]:
        """Get cost information for Vision API"""
        return {
            'cost_per_image_inr': 0.12,
            'cost_per_image_usd': 0.0015,
            'pricing_model': 'per_image',
            'description': 'Google Vision API Document Text Detection'
        }


# Test function
def test_vision_extractor():
    """Test Vision API extractor with sample image"""
    try:
        extractor = VisionExtractor()
        print("✅ Vision API extractor initialized successfully")
        print(f"💰 Cost estimate: ₹{extractor.get_cost_estimate()['cost_per_image_inr']} per image")
        return True
    except Exception as e:
        print(f"❌ Vision API extractor test failed: {e}")
        return False


if __name__ == "__main__":
    test_vision_extractor()