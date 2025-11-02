"""
Create Razorpay Subscription Plans
ONE-TIME SETUP SCRIPT

Run this script once to create all subscription plans in Razorpay.
Plans are reusable templates - create once, use for all customers.

Usage:
    python scripts/create_razorpay_plans.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.razorpay_service import razorpay_service
from app.config.plans import get_plan_config


def create_all_plans():
    """
    Create all subscription plans in Razorpay.
    
    This creates:
    - Basic Monthly Plan
    - Pro Monthly Plan
    - Ultra Monthly Plan
    - Max Monthly Plan
    """
    print("=" * 70)
    print("CREATING RAZORPAY SUBSCRIPTION PLANS")
    print("=" * 70)
    print()
    
    # Get pricing from actual plan configuration
    from app.config.plans import get_plan_config
    
    tiers = ["basic", "pro", "ultra", "max"]
    plans_to_create = []
    
    for tier in tiers:
        plan_config = get_plan_config(tier)
        plans_to_create.append({
            "tier": tier,
            "name": plan_config["name"],
            "base_price": plan_config["price_monthly"],  # Already GST-inclusive
            "period": "monthly",
            "interval": 1
        })
    
    created_plans = []
    failed_plans = []
    
    for plan_def in plans_to_create:
        tier = plan_def["tier"]
        amount = plan_def["base_price"]  # Already GST-inclusive
        
        # Convert to paise
        amount_paise = int(amount * 100)
        
        print(f"📝 Creating {plan_def['name']}...")
        print(f"   Amount (GST-inclusive): ₹{amount}")
        print(f"   Amount (paise): {amount_paise}")
        print()
        
        try:
            # Create plan (without custom ID - let Razorpay generate it)
            plan_id = razorpay_service.create_razorpay_plan(
                tier=tier,
                amount=amount_paise,
                interval=plan_def["interval"],
                period=plan_def["period"]
            )
            
            created_plans.append({
                "tier": tier,
                "plan_id": plan_id,
                "amount": amount
            })
            
            print(f"✅ SUCCESS: {plan_def['name']} created")
            print(f"   Plan ID: {plan_id}")
            print()
        
        except Exception as e:
            print(f"❌ FAILED: {plan_def['name']}")
            print(f"   Error: {str(e)}")
            print()
            
            failed_plans.append({
                "tier": tier,
                "error": str(e)
            })
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    
    if created_plans:
        print("✅ Successfully Created Plans:")
        for plan in created_plans:
            print(f"   - {plan['tier'].upper()}: {plan['plan_id']} (₹{plan['amount']:.2f}/month)")
        print()
    
    if failed_plans:
        print("❌ Failed Plans:")
        for plan in failed_plans:
            print(f"   - {plan['tier'].upper()}: {plan['error']}")
        print()
    
    print(f"Total: {len(created_plans)} created, {len(failed_plans)} failed")
    print()
    
    # Next steps
    if created_plans and not failed_plans:
        print("=" * 70)
        print("🎉 ALL PLANS CREATED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("1. ✅ Plans are now ready in Razorpay")
        print("2. 📝 Update database schema (add subscription columns)")
        print("3. 🔧 Update API endpoints to use subscriptions")
        print("4. 🧪 Test subscription flow")
        print()
        print("You can view plans in Razorpay Dashboard:")
        print("https://dashboard.razorpay.com/app/subscriptions/plans")
        print()
    elif failed_plans:
        print("⚠️ Some plans failed. Please check errors above.")
        print()
        return False
    
    return True


if __name__ == "__main__":
    try:
        # Check if Razorpay is configured
        if razorpay_service.key_id == 'rzp_test_dummy_key':
            print("❌ ERROR: Razorpay keys not configured!")
            print()
            print("Please set these environment variables:")
            print("  RAZORPAY_KEY_ID=your_key_id")
            print("  RAZORPAY_KEY_SECRET=your_key_secret")
            print()
            sys.exit(1)
        
        print(f"🔑 Using Razorpay Key: {razorpay_service.key_id}")
        print()
        
        # Create plans
        success = create_all_plans()
        
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print()
        print("❌ Aborted by user")
        sys.exit(1)
    
    except Exception as e:
        print()
        print(f"❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
