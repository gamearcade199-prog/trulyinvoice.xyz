#!/usr/bin/env python3
"""
QUICK FIX TEST: Check if the Gemini fallback is working
"""

print("🚀 QUICK DIAGNOSIS")
print("=" * 30)
print()
print("📋 ISSUE: Excel shows ₹0 even after fixes")
print()
print("🔍 POSSIBLE CAUSES:")
print("1. Gemini fallback not triggering")
print("2. Gemini fallback working but returning ₹0")
print("3. Database has old ₹0 records")
print("4. Frontend caching old data")
print()
print("🧪 TEST STEPS:")
print("1. Upload a NEW image invoice (not one uploaded before)")
print("2. Check backend logs for fallback messages")
print("3. Check if the NEW invoice shows correct amounts")
print()
print("💡 EXPECTED BACKEND LOGS:")
print("   📸 Image detected - using Vision API + Flash-Lite...")
print("   ❌ Vision API error: 403")  
print("   🔄 Vision API failed - trying Gemini-only fallback...")
print("   🤖 GEMINI-ONLY FALLBACK MODE")
print("   ✅ Gemini fallback: [VENDOR] - ₹[AMOUNT]")
print()
print("📤 Please upload a NEW image and report the backend logs!")

if __name__ == "__main__":
    pass