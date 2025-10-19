from fastapi import Request, HTTPException
from app.services.supabase_helper import supabase
from app.core.plan_limits import PLAN_LIMITS

async def check_subscription(request: Request):
    user_id = request.state.user_id
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Get user's plan
    user_plan = supabase.rpc('get_user_plan', {'user_id_in': user_id})
    if not user_plan.data:
        raise HTTPException(status_code=404, detail="User plan not found")

    plan = user_plan.data

    # Get user's usage
    usage_response = supabase.table('invoices').select('id', count='exact').eq('user_id', user_id).execute()
    
    # The new client returns a list-like object, so we check its length
    scan_count = len(usage_response.data)

    # Check if user has exceeded their limit
    if scan_count >= PLAN_LIMITS[plan]['scans']:
        raise HTTPException(status_code=403, detail="You have exceeded your scan limit. Please upgrade your plan.")
