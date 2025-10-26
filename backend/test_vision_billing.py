"""
VISION API BILLING & SETUP VERIFICATION
Check if Vision API is properly configured and billing is active
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment
backend_dir = Path(__file__).parent
env_path = backend_dir / ".env"
load_dotenv(env_path)

def check_vision_api_setup():
    """Verify Vision API setup and billing status"""
    print("🔍 VISION API SETUP VERIFICATION")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if not api_key:
        print("❌ GOOGLE_AI_API_KEY not found")
        return False
    
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT not found")
        return False
    
    print(f"✅ API Key: {api_key[:12]}...")
    print(f"✅ Project ID: {project_id}")
    
    # Test Vision API directly with a simple request
    print("\n🧪 Testing Vision API directly...")
    
    try:
        # Simple test image (1x1 white pixel as base64)
        test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        
        vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        
        payload = {
            "requests": [
                {
                    "image": {
                        "content": test_image_b64
                    },
                    "features": [
                        {
                            "type": "DOCUMENT_TEXT_DETECTION",
                            "maxResults": 1
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(vision_url, json=payload, timeout=30)
        
        print(f"📡 Vision API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Vision API is working! Billing is active!")
            result = response.json()
            print(f"   Response: {result}")
            return True
        elif response.status_code == 403:
            error_data = response.json()
            print("❌ Vision API billing issue:")
            print(f"   Status: {error_data.get('error', {}).get('status', 'Unknown')}")
            print(f"   Message: {error_data.get('error', {}).get('message', 'No message')}")
            
            # Check if it's a billing issue
            if "billing" in str(error_data).lower():
                print("\n💡 BILLING SETUP STEPS:")
                print("   1. Go to: https://console.cloud.google.com/billing")
                print(f"   2. Select project: {project_id}")
                print("   3. Link a billing account")
                print("   4. Enable Vision API: https://console.cloud.google.com/apis/library/vision.googleapis.com")
                print("   5. Wait 5-10 minutes for propagation")
            
            return False
        else:
            print(f"❌ Vision API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Vision API test failed: {e}")
        return False

def check_apis_enabled():
    """Check which APIs are enabled for the project"""
    print("\n🔧 CHECKING ENABLED APIS...")
    
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if not api_key or not project_id:
        print("❌ Missing API key or project ID")
        return
    
    try:
        # Check if Vision API is enabled
        url = f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services/vision.googleapis.com?key={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            service_data = response.json()
            state = service_data.get('state', 'UNKNOWN')
            print(f"✅ Vision API State: {state}")
            
            if state == 'ENABLED':
                print("✅ Vision API is enabled!")
            else:
                print("⚠️  Vision API might not be enabled")
                print(f"   Enable at: https://console.cloud.google.com/apis/library/vision.googleapis.com?project={project_id}")
        else:
            print(f"⚠️  Could not check API status: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Could not check APIs: {e}")

def billing_wait_test():
    """Wait and retry test for billing propagation"""
    print("\n⏳ BILLING PROPAGATION TEST")
    print("=" * 40)
    print("Google Cloud billing can take 5-10 minutes to propagate...")
    print("Testing every 30 seconds for 5 minutes...")
    
    import time
    max_attempts = 10  # 5 minutes
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n🔄 Attempt {attempt}/{max_attempts}")
        
        if check_vision_api_setup():
            print("🎉 VISION API IS NOW WORKING!")
            return True
        
        if attempt < max_attempts:
            print("⏳ Waiting 30 seconds...")
            time.sleep(30)
    
    print("\n❌ Vision API still not working after 5 minutes")
    print("💡 Try again in a few more minutes, or check billing setup")
    return False

if __name__ == "__main__":
    print("Starting Vision API verification...\n")
    
    # Initial check
    if check_vision_api_setup():
        print("\n🎉 VISION API IS READY!")
    else:
        print("\n⏳ Billing might still be propagating...")
        check_apis_enabled()
        
        # Ask user if they want to wait and retry
        print("\n❓ Do you want to wait and retry? This will test every 30 seconds for 5 minutes.")
        choice = input("Enter 'y' to wait and retry, or any other key to exit: ").lower()
        
        if choice == 'y':
            billing_wait_test()
        else:
            print("\n💡 Try running this test again in a few minutes!")