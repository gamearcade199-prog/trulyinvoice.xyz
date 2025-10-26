"""
Simple test script to manually process your stuck invoices
"""
import requests
import json

# Test 1: Check if backend is running
try:
    response = requests.get("http://localhost:8000/health")
    print("✅ Backend health check:", response.status_code)
    if response.status_code == 200:
        print(response.json())
except Exception as e:
    print("❌ Backend not running:", e)

# Test 2: Try to process document directly  
document_ids = [
    "8d3d4792-3a5b-4534-a442-8684dd8d28d1",
    # Add the second document ID if you know it
]

for doc_id in document_ids:
    try:
        print(f"\n🔄 Processing document: {doc_id}")
        response = requests.post(
            f"http://localhost:8000/api/documents/{doc_id}/process",
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Success!")
        else:
            print("❌ Failed")
            
    except Exception as e:
        print(f"❌ Error processing {doc_id}: {e}")

print("\n📋 Next steps:")
print("1. If backend crashed, restart it")
print("2. If processing failed, check the error message")
print("3. Try refreshing your invoices page")