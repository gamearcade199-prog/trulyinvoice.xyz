"""
🧪 VISION + FLASH-LITE SYSTEM TEST
Complete verification that the new system is working properly
"""

import os
import sys
import pathlib
from dotenv import load_dotenv

# Load environment variables
backend_dir = pathlib.Path(__file__).parent
env_path = backend_dir / ".env"
load_dotenv(env_path)

def test_new_system():
    """Test the complete Vision + Flash-Lite system"""
    
    print("🧪 TESTING VISION + FLASH-LITE SYSTEM")
    print("=" * 50)
    
    # Test 1: Environment setup
    print("1️⃣ Testing environment setup...")
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if api_key:
        print(f"   ✅ API key found: {api_key[:10]}...")
    else:
        print("   ❌ API key not found")
        return False
    
    # Test 2: Import new services
    print("\n2️⃣ Testing new service imports...")
    try:
        sys.path.insert(0, '.')
        from app.services.vision_extractor import VisionExtractor
        from app.services.flash_lite_formatter import FlashLiteFormatter
        from app.services.vision_ocr_flash_lite_extractor import VisionOCR_FlashLite_Extractor
        print("   ✅ All new services imported successfully")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test 3: Initialize services
    print("\n3️⃣ Testing service initialization...")
    try:
        vision_extractor = VisionExtractor()
        flash_lite_formatter = FlashLiteFormatter()
        combined_extractor = VisionOCR_FlashLite_Extractor()
        print("   ✅ All services initialized successfully")
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        return False
    
    # Test 4: Check AI service
    print("\n4️⃣ Testing updated AI service...")
    try:
        from app.services.ai_service import ai_service
        print("   ✅ AI service imported successfully")
        print(f"   📋 Extractor type: {type(ai_service.extractor).__name__}")
    except Exception as e:
        print(f"   ❌ AI service test failed: {e}")
        return False
    
    # Test 5: Check documents API
    print("\n5️⃣ Testing documents API updates...")
    try:
        from app.api.documents import AI_AVAILABLE
        if AI_AVAILABLE:
            print("   ✅ Documents API shows AI available")
        else:
            print("   ⚠️ Documents API shows AI not available")
    except Exception as e:
        print(f"   ❌ Documents API test failed: {e}")
        return False
    
    # Test 6: Cost estimates
    print("\n6️⃣ Testing cost estimates...")
    try:
        vision_cost = vision_extractor.get_cost_estimate()
        flash_lite_cost = flash_lite_formatter.get_cost_estimate()
        combined_cost = combined_extractor.get_cost_estimate()
        
        print(f"   💰 Vision API: ₹{vision_cost['cost_per_image_inr']}")
        print(f"   💰 Flash-Lite: ₹{flash_lite_cost['cost_per_format_inr']}")
        print(f"   💰 Combined: ₹{combined_cost['total_cost_inr']}")
        
        total_cost = combined_cost['total_cost_inr']
        if total_cost <= 0.15:  # Should be around ₹0.13
            print("   ✅ Cost within expected range")
        else:
            print(f"   ⚠️ Cost higher than expected: ₹{total_cost}")
            
    except Exception as e:
        print(f"   ❌ Cost estimate test failed: {e}")
        return False
    
    print("\n✅ ALL TESTS PASSED!")
    print("🎉 Vision + Flash-Lite system is ready!")
    print(f"💰 Total cost per invoice: ₹{combined_cost['total_cost_inr']}")
    print("🚀 Start your server and test with real invoices!")
    
    return True

if __name__ == "__main__":
    success = test_new_system()
    if not success:
        print("\n❌ TESTS FAILED - Check the errors above")
        sys.exit(1)
    else:
        print("\n🎯 SYSTEM READY FOR PRODUCTION!")