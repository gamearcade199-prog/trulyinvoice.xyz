#!/usr/bin/env python3
"""
TEST GEMINI EXTRACTOR DIRECTLY: Skip Vision API and test Gemini directly
"""

import os
import base64
import sys

def test_gemini_direct():
    """Test Gemini extractor directly with image"""
    
    print("🤖 TESTING GEMINI EXTRACTOR DIRECTLY")
    print("=" * 50)
    print()
    
    # Check if we can import the Gemini extractor
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        from app.services.gemini_extractor import GeminiExtractor
        
        print("✅ GeminiExtractor imported successfully")
        
        # Check API key
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            print("❌ GOOGLE_AI_API_KEY not found in environment")
            print("💡 Make sure API key is set in backend/.env")
            return
        
        print(f"✅ API key found: {api_key[:10]}...")
        
        # Initialize extractor
        extractor = GeminiExtractor()
        print("✅ Gemini extractor initialized")
        
        print()
        print("🧪 TO TEST WITH YOUR INVOICE IMAGE:")
        print("1. Save your invoice image as 'test_invoice.jpg' in this directory")
        print("2. Run this script again")
        print("3. It will test Gemini extraction directly")
        
        # Check if test image exists
        test_image_path = "test_invoice.jpg"
        if os.path.exists(test_image_path):
            print(f"📸 Found test image: {test_image_path}")
            print("🔄 Testing extraction...")
            
            # Test extraction
            result = extractor.extract_from_image(image_path=test_image_path)
            
            if result:
                print("✅ EXTRACTION SUCCESSFUL!")
                print(f"📋 Vendor: {result.get('vendor_name', 'N/A')}")
                print(f"💰 Total: ₹{result.get('total_amount', 0)}")
                print(f"📄 Invoice Number: {result.get('invoice_number', 'N/A')}")
                print(f"🎯 Fields extracted: {len(result)} fields")
                
                if result.get('total_amount', 0) > 0:
                    print("🎉 SUCCESS: Non-zero amount extracted!")
                else:
                    print("❌ ISSUE: Still getting zero amount")
            else:
                print("❌ EXTRACTION FAILED: No result returned")
        else:
            print(f"💡 Place your invoice image as '{test_image_path}' to test")
        
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        print("💡 Make sure backend dependencies are installed")

if __name__ == "__main__":
    test_gemini_direct()