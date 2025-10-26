"""
Test OpenAI API Key directly
"""
import asyncio
import os

# Set API key
os.environ['OPENAI_API_KEY'] = 'YOUR_NEW_OPENAI_API_KEY_HERE'

async def test_openai():
    from openai import OpenAI
    
    print("=" * 80)
    print("🧪 TESTING OPENAI API KEY")
    print("=" * 80)
    
    try:
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        
        print("\n1️⃣  Testing API connection...")
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Return only valid JSON."},
                {"role": "user", "content": 'Extract data from this text and return JSON: "Invoice #123 from Acme Corp for $500"'}
            ],
            temperature=0,
            max_tokens=100
        )
        
        print("✅ API Response received!")
        print(f"\nResponse:")
        print(response.choices[0].message.content)
        print("\n✅ OpenAI API is working correctly!")
        
    except Exception as e:
        print(f"\n❌ OpenAI API Error: {e}")
        print(f"\nError type: {type(e).__name__}")
        
        if "invalid" in str(e).lower() or "authentication" in str(e).lower():
            print("\n🔑 API Key Issue:")
            print("   Your API key may be:")
            print("   - Expired")
            print("   - Invalid")
            print("   - Out of credits")
            print("\n💡 Solution:")
            print("   1. Go to https://platform.openai.com/api-keys")
            print("   2. Create a NEW API key")
            print("   3. Replace in backend/.env file")
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_openai())
