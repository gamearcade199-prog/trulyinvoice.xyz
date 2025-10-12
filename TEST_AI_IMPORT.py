"""
Test if AI extraction is working
"""
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ai_extractor import SimpleAIExtractor
from dotenv import load_dotenv

load_dotenv('backend/.env')

api_key = os.getenv("OPENAI_API_KEY")

print(f"🔑 API Key loaded: {'✅' if api_key else '❌'}")
print(f"🔑 Key starts with: {api_key[:10]}...")

# Test extraction
extractor = SimpleAIExtractor(api_key)

test_text = """
Tax invoice ID: ADS438-104904172
Paid: 1,895.68 INR
Subtotal: 1,606.51 INR
IGST (18%): 289.17 INR
Facebook India Online Services Pvt. Ltd.
"""

print("\n🤖 Testing AI extraction...")
result = extractor.extract_from_text(test_text)

if result:
    print("✅ AI Extraction WORKING!")
    print(f"   Total: ₹{result.get('total_amount')}")
else:
    print("❌ AI Extraction FAILED")
