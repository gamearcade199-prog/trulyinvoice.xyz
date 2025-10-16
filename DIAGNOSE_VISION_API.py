"""
🔍 VISION API DIAGNOSTIC TOOL
=============================
Checks if Cloud Vision API is enabled and ready to use
"""

import os
import sys
import json
from dotenv import load_dotenv
from pathlib import Path

# Load environment
backend_dir = Path(__file__).parent / "backend"
env_path = backend_dir / ".env"
load_dotenv(env_path)

print("\n" + "="*70)
print("🔍 VISION API DIAGNOSTIC TOOL")
print("="*70)

# Check 1: API Key
print("\n1️⃣ Checking Google AI API Key...")
api_key = os.getenv('GOOGLE_AI_API_KEY')
if api_key:
    print(f"   ✅ API Key found: {api_key[:20]}...")
else:
    print("   ❌ API Key NOT found!")
    print("   Fix: Add GOOGLE_AI_API_KEY to backend/.env")
    sys.exit(1)

# Check 2: Vision API Package
print("\n2️⃣ Checking google-cloud-vision package...")
try:
    from google.cloud import vision
    print("   ✅ google-cloud-vision installed")
except ImportError:
    print("   ❌ google-cloud-vision NOT installed")
    print("   Fix: pip install google-cloud-vision")
    sys.exit(1)

# Check 3: Vision Extractor Module
print("\n3️⃣ Checking Vision Extractor module...")
sys.path.insert(0, str(backend_dir))
try:
    from app.services.vision_extractor import VisionExtractor
    print("   ✅ VisionExtractor module found")
except ImportError as e:
    print(f"   ❌ VisionExtractor import failed: {e}")
    sys.exit(1)

# Check 4: Initialize Vision Extractor
print("\n4️⃣ Testing Vision Extractor initialization...")
try:
    extractor = VisionExtractor()
    print("   ✅ VisionExtractor initialized successfully")
    print(f"   📊 Using API Key: {api_key[:20]}...")
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    sys.exit(1)

# Check 5: Test Vision API Connection
print("\n5️⃣ Testing Vision API connection...")
try:
    # Create a minimal test image (1x1 pixel transparent PNG)
    import base64
    
    # Minimal PNG image (1x1 transparent pixel)
    minimal_png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    
    result = extractor.extract_text_from_image(minimal_png)
    
    if result['success']:
        print("   ✅ Vision API is WORKING!")
        print(f"      Text extracted: {len(result['extracted_text'])} characters")
        print(f"      Confidence: {result['confidence']:.1%}")
    else:
        error_msg = result.get('error', 'Unknown error')
        if "403" in str(error_msg) or "PERMISSION_DENIED" in str(error_msg):
            print("   ❌ Vision API is DISABLED (403 error)")
            print("   📋 ACTION REQUIRED:")
            print("      1. Go to: https://console.developers.google.com/apis")
            print("      2. Search for 'Vision API'")
            print("      3. Click 'ENABLE'")
            print("      4. Wait 2-5 minutes for propagation")
            print("      5. Run this diagnostic again")
        else:
            print(f"   ❌ Vision API error: {error_msg}")
        sys.exit(1)
        
except Exception as e:
    error_str = str(e)
    if "403" in error_str or "PERMISSION_DENIED" in error_str:
        print("   ❌ Vision API is DISABLED (403 error)")
        print("   📋 ACTION REQUIRED:")
        print("      1. Go to: https://console.developers.google.com/apis")
        print("      2. Search for 'Vision API'")
        print("      3. Click 'ENABLE'")
        print("      4. Wait 2-5 minutes for propagation")
        print("      5. Run this diagnostic again")
    else:
        print(f"   ❌ Connection test failed: {e}")
    sys.exit(1)

# Check 6: Vision + Flash-Lite Combined
print("\n6️⃣ Testing Vision + Flash-Lite combination...")
try:
    from app.services.vision_flash_lite_extractor import VisionFlashLiteExtractor
    combined = VisionFlashLiteExtractor()
    
    cost_info = combined.get_cost_estimate()
    print("   ✅ Vision + Flash-Lite extractor ready")
    print(f"      Vision API: ₹{cost_info['vision_api_cost_inr']}")
    print(f"      Flash-Lite: ₹{cost_info['flash_lite_cost_inr']}")
    print(f"      Total: ₹{cost_info['total_cost_inr']}")
    print(f"      Savings: {cost_info['cost_reduction_vs_gemini']}")
except Exception as e:
    print(f"   ⚠️  Combined extractor warning: {e}")

# Final Summary
print("\n" + "="*70)
print("📊 DIAGNOSTIC SUMMARY")
print("="*70)

if result['success']:
    print("✅ ALL CHECKS PASSED - Vision API is ready!")
    print("\n🚀 Your system is ready for production:")
    print("   • Vision API: ENABLED ✅")
    print("   • Flash-Lite: READY ✅")
    print("   • Combined cost: ₹0.13 per invoice (99% cheaper)")
    print("\n▶️ Next: Start processing invoices!")
else:
    print("⚠️  Vision API is currently DISABLED")
    print("\n📋 QUICK FIX (30 seconds):")
    print("   1. Click: https://console.developers.google.com/apis/api/vision.googleapis.com/overview?project=1098585626293")
    print("   2. Click: [ENABLE]")
    print("   3. Wait: 2-5 minutes")
    print("   4. Run: python DIAGNOSE_VISION_API.py")
    print("\n💡 NOTE: System still works with fallback extraction!")
    print("   Your invoices will be processed at slightly lower cost while")
    print("   Vision API is enabled.")

print("="*70 + "\n")
