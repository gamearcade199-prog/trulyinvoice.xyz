"""
Fix Razorpay Plans - Recreate with Correct Pricing
This script recreates plans with correct pricing from plans.py configuration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.razorpay_service import razorpay_service
from app.config.plans import get_plan_config


def main():
    print("=" * 70)
    print("FIXING RAZORPAY SUBSCRIPTION PLANS")
    print("=" * 70)
    print()
    
    print("📋 Current incorrect plans in Razorpay:")
    print("   - Basic: ₹149/month ✅ (correct)")
    print("   - Pro: ₹499/month ❌ (should be ₹299)")
    print("   - Ultra: ₹1001/month ❌ (should be ₹599)")
    print("   - Max: ₹1999/month ❌ (should be ₹999)")
    print()
    
    print("⚠️ IMPORTANT:")
    print("   Razorpay doesn't allow deleting plans via API.")
    print("   Old plans will remain but we'll create new correct ones.")
    print("   You can manually archive old plans in Razorpay Dashboard.")
    print()
    
    input("Press Enter to create correct plans (or Ctrl+C to cancel)...")
    print()
    
    # Get correct pricing from configuration
    tiers = ["basic", "pro", "ultra", "max"]
    
    for tier in tiers:
        plan_config = get_plan_config(tier)
        amount = plan_config["price_monthly"]
        amount_paise = int(amount * 100)
        
        print(f"📝 Creating {plan_config['name']}...")
        print(f"   Correct Amount: ₹{amount}/month")
        print(f"   Scans: {plan_config['scans_per_month']}/month")
        
        try:
            plan_id = razorpay_service.create_razorpay_plan(
                tier=tier,
                amount=amount_paise,
                interval=1,
                period="monthly"
            )
            
            print(f"✅ Plan created: {plan_id}")
            print()
        
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            print()
    
    print("=" * 70)
    print("✅ CORRECT PLANS CREATED")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Go to: https://dashboard.razorpay.com/app/subscriptions/plans")
    print("2. You'll see both old and new plans")
    print("3. The new plans will be used going forward")
    print("4. Optionally: Contact Razorpay to archive old plans")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
