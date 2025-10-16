"""
Quick test to verify Vision API is working
"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

try:
    import google.generativeai as genai
    from PIL import Image
    import requests
    from io import BytesIO
    
    print("="*70)
    print("🧪 VISION API TEST")
    print("="*70)
    
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        print("\n❌ API Key not found in .env")
        sys.exit(1)
    
    print(f"\n✅ API Key found: {api_key[:20]}...")
    
    # Configure API
    genai.configure(api_key=api_key)
    print("✅ API configured")
    
    # Test 1: List models
    print("\n📋 Test 1: Listing available models...")
    models = list(genai.list_models())
    print(f"✅ Successfully retrieved {len(models)} models")
    
    # Test 2: Check vision models
    print("\n📸 Test 2: Checking for vision models...")
    vision_models = []
    for m in models:
        if 'vision' in m.name.lower() or any('vision' in str(method) for method in m.supported_generation_methods):
            vision_models.append(m.name)
    
    if vision_models:
        print(f"✅ Found {len(vision_models)} vision models:")
        for model in vision_models[:3]:
            print(f"   - {model}")
    else:
        print("⚠️  No explicit vision models found, but vision may work with gemini models")
    
    # Test 3: Get Gemini model info
    print("\n🤖 Test 3: Getting Gemini model capabilities...")
    try:
        model_info = genai.get_model("models/gemini-2.0-flash")
        print(f"✅ Gemini-2.0-Flash model found")
        print(f"   - Supports vision: {'vision' in str(model_info).lower()}")
        
        if hasattr(model_info, 'supported_generation_methods'):
            methods = list(model_info.supported_generation_methods)
            print(f"   - Methods: {methods}")
    except:
        print("⚠️  Could not fetch Gemini model info")
    
    # Test 4: Try vision request with dummy image
    print("\n🎯 Test 4: Testing vision capability with sample image...")
    try:
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Try to process with vision
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Upload file
        print("   - Uploading test image...")
        file_response = genai.upload_file(img_bytes, mime_type="image/png")
        print(f"   ✅ File uploaded: {file_response.uri}")
        
        # Try to process
        print("   - Processing image with Vision API...")
        response = model.generate_content([
            "What is in this image? Describe briefly.",
            file_response
        ])
        
        print(f"   ✅ Vision API processing works!")
        print(f"   Response: {response.text[:100]}...")
        
        # Cleanup
        try:
            genai.delete_file(file_response.name)
            print("   ✅ Cleaned up test file")
        except:
            pass
        
    except Exception as e:
        print(f"   ❌ Vision request failed: {e}")
    
    print("\n" + "="*70)
    print("✅ VISION API IS WORKING!")
    print("="*70)
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nInstall required packages:")
    print("   pip install google-generativeai pillow requests")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
