"""
🔍 RENDER API KEY DIAGNOSTIC
Run this on your local backend to simulate what Render sees
"""

import os

print("\n" + "="*60)
print("🔍 API KEY DIAGNOSTIC - CHECKING ALL POSSIBLE VARIABLES")
print("="*60)

# Check all possible API key variable names
possible_keys = [
    'GOOGLE_AI_API_KEY',
    'GEMINI_API_KEY',
    'GOOGLE_GENERATIVE_AI_KEY',
    'GENAI_API_KEY',
    'GOOGLE_API_KEY',
    'ANTHROPIC_API_KEY',
    'OPENAI_API_KEY'
]

print("\n✅ Checking environment variables:")
for key_name in possible_keys:
    value = os.getenv(key_name)
    if value:
        print(f"   ✅ {key_name}: {value[:10]}...{value[-5:]}")
    else:
        print(f"   ❌ {key_name}: NOT SET")

# Check which one the code is actually using
print("\n✅ Checking which key the code tries to use:")
code_uses = 'GOOGLE_AI_API_KEY'
value = os.getenv(code_uses)
if value:
    print(f"   ✅ Code looks for: {code_uses}")
    print(f"   ✅ FOUND: {value[:10]}...{value[-5:]}")
else:
    print(f"   ❌ Code looks for: {code_uses}")
    print(f"   ❌ NOT FOUND - This is the problem!")

# Test Gemini initialization
print("\n✅ Testing Gemini initialization:")
try:
    import google.generativeai as genai
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    
    if not api_key:
        print("   ❌ GOOGLE_AI_API_KEY not found")
        print("   💡 Try setting: GOOGLE_AI_API_KEY instead of GEMINI_API_KEY")
    else:
        genai.configure(api_key=api_key)
        print(f"   ✅ Gemini configured successfully")
        
        # Try to list models
        models = genai.list_models()
        print(f"   ✅ Can access Gemini API")
        print(f"   ✅ Available models: {len(list(models))} found")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("🔧 SOLUTION:")
print("="*60)
print("""
If GOOGLE_AI_API_KEY shows as NOT SET:

On Render dashboard:
1. Go to Backend service → Environment
2. Make sure variable name is exactly: GOOGLE_AI_API_KEY
3. Not: GEMINI_API_KEY
4. Not: GOOGLE_API_KEY
5. Exact match: GOOGLE_AI_API_KEY

Then restart the service.
""")
print("="*60 + "\n")
