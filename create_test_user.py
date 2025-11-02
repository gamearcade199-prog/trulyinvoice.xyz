"""
Create a test user for TrulyInvoice
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('frontend/.env.local')

# Supabase credentials
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# Test user credentials
TEST_EMAIL = "test@trulyinvoice.com"
TEST_PASSWORD = "Test@123456"

def create_test_user():
    try:
        # Initialize Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("🔧 Creating test user...")
        print(f"📧 Email: {TEST_EMAIL}")
        print(f"🔑 Password: {TEST_PASSWORD}")
        print()
        
        # Try to sign up the user
        try:
            response = supabase.auth.sign_up({
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD,
                "options": {
                    "data": {
                        "full_name": "Test User",
                        "plan": "free"
                    }
                }
            })
            
            if response.user:
                print("✅ Test user created successfully!")
                print(f"   User ID: {response.user.id}")
                print(f"   Email: {response.user.email}")
                print()
                print("📝 Login Credentials:")
                print(f"   Email: {TEST_EMAIL}")
                print(f"   Password: {TEST_PASSWORD}")
                print()
                print("🌐 Frontend URL: http://localhost:3000")
                print("🔐 Login URL: http://localhost:3000/login")
            else:
                print("⚠️  User creation response received but no user object")
                
        except Exception as signup_error:
            error_msg = str(signup_error)
            
            # Check if user already exists
            if "already registered" in error_msg.lower() or "already exists" in error_msg.lower():
                print("ℹ️  Test user already exists!")
                print()
                print("📝 Existing Login Credentials:")
                print(f"   Email: {TEST_EMAIL}")
                print(f"   Password: {TEST_PASSWORD}")
                print()
                print("🌐 Frontend URL: http://localhost:3000")
                print("🔐 Login URL: http://localhost:3000/login")
                print()
                print("💡 Tip: If you forgot the password, use the 'Forgot Password' link")
            else:
                print(f"❌ Error creating user: {error_msg}")
                raise
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("  TRULYINVOICE - TEST USER SETUP")
    print("=" * 60)
    print()
    
    success = create_test_user()
    
    if success:
        print()
        print("=" * 60)
        print("  ✅ SETUP COMPLETE - YOU CAN NOW LOGIN!")
        print("=" * 60)
