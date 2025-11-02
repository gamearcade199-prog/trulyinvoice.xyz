"""
Create CORRECT Razorpay Subscription Plans (v2)
Uses actual pricing from plans.py configuration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.razorpay_service import razorpay_service
from app.config.plans import get_plan_config


def create_correct_plans():
    """Create plans with correct pricing from plans.py"""
    
    print("=" * 70)
    print("CREATING CORRECT RAZORPAY SUBSCRIPTION PLANS (V2)")
    print("=" * 70)
    print()
    
    print("📋 Target Pricing (from plans.py):")
    print("   - Basic: ₹149/month")
    print("   - Pro: ₹299/month")
    print("   - Ultra: ₹599/month")
    print("   - Max: ₹999/month")
    print()
    
    tiers = ["basic", "pro", "ultra", "max"]
    created_plans = []
    
    for tier in tiers:
        plan_config = get_plan_config(tier)
        amount = plan_config["price_monthly"]
        amount_paise = int(amount * 100)
        
        print(f"📝 Creating {plan_config['name']} (CORRECT PRICING)...")
        print(f"   Amount: ₹{amount}/month")
        print(f"   Amount (paise): {amount_paise}")
        print(f"   Scans: {plan_config['scans_per_month']}/month")
        
        try:
            # Create plan with correct pricing
            # Use v2 internal ID to differentiate from old plans
            internal_id = f"trulyinvoice_{tier}_monthly_v2"
            
            plan = razorpay_service.client.plan.create({
                "period": "monthly",
                "interval": 1,
                "item": {
                    "name": f"TrulyInvoice {tier.title()} Plan",
                    "amount": amount_paise,
                    "currency": "INR",
                    "description": f"{plan_config['name']} - {plan_config['scans_per_month']} scans/month"
                },
                "notes": {
                    "tier": tier,
                    "internal_id": internal_id,
                    "version": "v2",
                    "created_via": "api",
                    "scans_limit": str(plan_config['scans_per_month']),
                    "correct_pricing": "true"
                }
            })
            
            plan_id = plan.get("id")
            created_plans.append({
                "tier": tier,
                "plan_id": plan_id,
                "amount": amount,
                "internal_id": internal_id
            })
            
            print(f"✅ Plan created: {plan_id}")
            print(f"   Internal ID: {internal_id}")
            print()
        
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    
    if created_plans:
        print("✅ Successfully Created Correct Plans:")
        for plan in created_plans:
            print(f"   {plan['tier'].upper():6} → {plan['plan_id']} (₹{plan['amount']}/month)")
        print()
        
        print("📝 Plan IDs to use in your application:")
        print()
        for plan in created_plans:
            print(f"   {plan['tier']}: {plan['plan_id']}")
        print()
        
        print("=" * 70)
        print("🎉 CORRECT PLANS READY!")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("1. ✅ Correct plans created in Razorpay")
        print("2. 📝 Code will automatically use v2 plans")
        print("3. 🗑️ Old incorrect plans can be archived manually")
        print("4. 🧪 Test subscription creation")
        print()
    else:
        print("❌ No plans created. Check errors above.")
        print()


if __name__ == "__main__":
    try:
        create_correct_plans()
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
