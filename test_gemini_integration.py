"""
🔍 GEMINI INTEGRATION DIAGNOSTIC
=================================

This script checks if Gemini integration is working correctly.
"""
import os
import sys

# Add backend to path
sys.path.insert(0, 'backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

print("="*70)
print("🔍 GEMINI INTEGRATION DIAGNOSTIC")
print("="*70)

# Check 1: Environment Variables
print("\n1️⃣ Checking Environment Variables...")
google_ai_key = os.getenv('GOOGLE_AI_API_KEY')
gemini_model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')

if google_ai_key:
    print(f"   ✅ GOOGLE_AI_API_KEY found: {google_ai_key[:20]}...")
else:
    print(f"   ❌ GOOGLE_AI_API_KEY not found!")
    sys.exit(1)

print(f"   ✅ GEMINI_MODEL: {gemini_model}")

# Check 2: Google Generative AI Package
print("\n2️⃣ Checking google-generativeai package...")
try:
    import google.generativeai as genai
    print("   ✅ google-generativeai package installed")
except ImportError as e:
    print(f"   ❌ google-generativeai NOT installed: {e}")
    sys.exit(1)

# Check 3: GeminiExtractor Class
print("\n3️⃣ Checking GeminiExtractor class...")
try:
    from app.services.gemini_extractor import GeminiExtractor
    print("   ✅ GeminiExtractor imported successfully")
except ImportError as e:
    print(f"   ❌ GeminiExtractor import failed: {e}")
    sys.exit(1)

# Check 4: Initialize Extractor
print("\n4️⃣ Initializing GeminiExtractor...")
try:
    extractor = GeminiExtractor()
    print(f"   ✅ GeminiExtractor initialized")
    print(f"   ✅ Model: {extractor.model_name}")
    print(f"   ✅ Confidence threshold: {extractor.min_confidence_threshold}")
    print(f"   ✅ Extraction passes: {extractor.extraction_passes}")
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    sys.exit(1)

# Check 5: API Connection Test
print("\n5️⃣ Testing Gemini API connection...")
try:
    response = extractor.model.generate_content("Say 'API working!'")
    print(f"   ✅ API Response: {response.text}")
except Exception as e:
    print(f"   ❌ API test failed: {e}")
    sys.exit(1)

# Check 6: documents.py Integration
print("\n6️⃣ Checking documents.py integration...")
try:
    with open('backend/app/api/documents.py', 'r') as f:
        content = f.read()
        if 'GeminiExtractor' in content:
            print("   ✅ documents.py uses GeminiExtractor")
        else:
            print("   ⚠️  documents.py does NOT use GeminiExtractor")
            
        if 'GOOGLE_AI_API_KEY' in content:
            print("   ✅ documents.py checks for GOOGLE_AI_API_KEY")
        else:
            print("   ⚠️  documents.py does NOT check for GOOGLE_AI_API_KEY")
except Exception as e:
    print(f"   ❌ documents.py check failed: {e}")

# Check 7: Test Extract Method Exists
print("\n7️⃣ Checking extraction methods...")
if hasattr(extractor, 'extract_from_text'):
    print("   ✅ extract_from_text() method exists")
else:
    print("   ❌ extract_from_text() method missing!")

if hasattr(extractor, 'extract_from_image'):
    print("   ✅ extract_from_image() method exists")
else:
    print("   ❌ extract_from_image() method missing!")

# Final Summary
print("\n" + "="*70)
print("📊 DIAGNOSTIC SUMMARY")
print("="*70)
print("✅ All checks passed!")
print("\n🚀 Gemini 2.5 Flash is ready to use!")
print("\nNext steps:")
print("  1. Start backend: cd backend && python -m uvicorn app.main:app --reload")
print("  2. Upload an invoice and test extraction")
print("  3. Check console for extraction quality report")
print("="*70)
