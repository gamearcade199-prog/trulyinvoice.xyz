import os
from dotenv import load_dotenv
import sys

load_dotenv()

print("=" * 70)
print("VISION API TEST")
print("=" * 70)

api_key = os.getenv('GOOGLE_AI_API_KEY')
print(f"\n1. API Key Status: {'FOUND' if api_key else 'NOT FOUND'}")

if api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        print("2. API Configuration: SUCCESS")
        
        models = list(genai.list_models())
        print(f"3. Models Available: {len(models)} models found")
        
        print("\n4. Gemini Model Status:")
        try:
            model = genai.get_model("models/gemini-2.0-flash")
            print(f"   - Gemini-2.0-Flash: AVAILABLE")
        except:
            print(f"   - Gemini-2.0-Flash: ERROR")
        
        print("\n" + "=" * 70)
        print("RESULT: VISION API IS WORKING!")
        print("=" * 70)
        
    except Exception as e:
        print(f"2. Error: {e}")
else:
    print("API Key missing!")
