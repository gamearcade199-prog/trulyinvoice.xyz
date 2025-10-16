#!/usr/bin/env python3
"""
DEBUG GEMINI FALLBACK: Test if the fallback is working for images
"""

import requests
import json

def test_gemini_fallback():
    """Test if Gemini fallback is actually working for image processing"""
    
    print("🔍 TESTING GEMINI FALLBACK FUNCTIONALITY")
    print("=" * 50)
    print()
    
    # Check backend logs for recent processing
    backend_url = "http://localhost:8000"
    
    print(f"📡 Backend URL: {backend_url}")
    print()
    
    # Test with a health check first
    try:
        response = requests.get(f"{backend_url}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    print()
    print("🔍 WHAT TO LOOK FOR IN BACKEND LOGS:")
    print("1. When you upload an image, look for:")
    print("   📸 'Image detected - using Vision API + Flash-Lite...'")
    print("   ❌ 'Vision API error: 403'")
    print("   🔄 'Vision API failed - trying Gemini-only fallback...'")
    print("   🤖 'GEMINI-ONLY FALLBACK MODE'")
    print()
    print("2. If you DON'T see the fallback messages, the fix isn't working")
    print("3. If you DO see them but still get ₹0, there's an issue with Gemini extraction")
    print()
    print("💡 NEXT STEPS:")
    print("1. Upload an image invoice at http://localhost:3002")
    print("2. Watch the backend terminal for these log messages")
    print("3. Report back what you see!")

if __name__ == "__main__":
    test_gemini_fallback()