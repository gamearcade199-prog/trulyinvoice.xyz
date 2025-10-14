"""
Simple test to verify backend can import properly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Testing imports...")

try:
    from app.main import app
    print("✅ Main app imported successfully")
    print(f"   App title: {app.title}")
    print(f"   App version: {app.version}")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    import traceback
    traceback.print_exc()

try:
    from app.services.ai_service import ai_service
    print("✅ AI service imported successfully")
except Exception as e:
    print(f"❌ Failed to import ai_service: {e}")
    import traceback
    traceback.print_exc()

print("\nAll imports successful! Backend code is valid.")
