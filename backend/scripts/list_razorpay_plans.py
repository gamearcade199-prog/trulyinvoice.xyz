"""
List All Razorpay Plans
Shows all plans currently in your Razorpay account
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.razorpay_service import razorpay_service


def list_all_plans():
    """List all plans in Razorpay account"""
    
    print("=" * 70)
    print("RAZORPAY SUBSCRIPTION PLANS")
    print("=" * 70)
    print()
    
    try:
        # Fetch all plans
        plans_response = razorpay_service.client.plan.all()
        
        if isinstance(plans_response, dict):
            plans = plans_response.get("items", [])
        else:
            plans = list(plans_response) if plans_response else []
        
        if not plans:
            print("⚠️ No plans found")
            return
        
        print(f"Found {len(plans)} plans:\n")
        
        for i, plan in enumerate(plans, 1):
            plan_id = plan.get("id")
            item = plan.get("item", {})
            name = item.get("name", "Unknown")
            amount = item.get("amount", 0) / 100  # Convert from paise
            currency = item.get("currency", "INR")
            period = plan.get("period")
            interval = plan.get("interval")
            notes = plan.get("notes", {})
            
            print(f"Plan {i}:")
            print(f"  ID: {plan_id}")
            print(f"  Name: {name}")
            print(f"  Amount: {currency} {amount}")
            print(f"  Billing: Every {interval} {period}(s)")
            print(f"  Internal ID: {notes.get('internal_id', 'N/A')}")
            print(f"  Tier: {notes.get('tier', 'N/A')}")
            print()
        
        print("=" * 70)
        print("To use these plans in your app, the code will automatically")
        print("select the correct plan based on tier.")
        print("=" * 70)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    list_all_plans()
