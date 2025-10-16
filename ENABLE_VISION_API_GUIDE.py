#!/usr/bin/env python3
"""
ENABLE VISION API: Instructions to enable Vision API for image invoice extraction
"""

print("🔧 VISION API SETUP GUIDE")
print("=" * 50)
print()
print("📋 ISSUE: Vision API is blocked, causing ₹0 extraction for images")
print("   ✅ PDFs work: Text extraction → Flash-Lite → Correct amounts")
print("   ❌ Images fail: Vision API blocked → Fallback → ₹0 amounts")
print()
print("🎯 SOLUTION: Enable Vision API in Google Cloud Console")
print()
print("📝 STEPS:")
print("1. Go to: https://console.cloud.google.com/")
print("2. Select your project: projects/1098585626293")
print("3. Navigate to: APIs & Services > Library")
print("4. Search for: 'Cloud Vision API'")
print("5. Click: ENABLE")
print("6. Wait 2-3 minutes for activation")
print()
print("💡 ALTERNATIVE: Use Gemini-only mode (images → text)")
print("   This would convert images to text first, then process like PDFs")
print()
print("🚀 AFTER ENABLING:")
print("   - Images: Vision API → Flash-Lite → Accurate amounts")
print("   - PDFs: Direct text → Flash-Lite → Accurate amounts")
print("   - Cost: ~₹0.05 per image (very low)")

if __name__ == "__main__":
    pass