"""
Subscription Plan Configuration
Defines all plan limits, features, and pricing tiers
"""

from typing import Dict, List, Any
from enum import Enum

class PlanTier(str, Enum):
    """Plan tier enumeration"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ULTRA = "ultra"
    MAX = "max"


# Plan Limits and Features Configuration
PLAN_LIMITS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": PlanTier.FREE,
        "name": "Free Plan",
        "price_monthly": 0,
        "price_yearly": 0,
        "scans_per_month": 10,
        "storage_days": 1,
        "bulk_upload_limit": 1,
        "ai_accuracy": "Basic",
        "features": [
            "basic_ai_extraction",
            "pdf_image_support",
            "email_support",
            "1_day_storage",
            "excel_csv_export"  # Allow full Excel and CSV export for free users
        ],
        "rate_limits": {
            "api_requests_per_minute": 10,
            "api_requests_per_hour": 100,
            "api_requests_per_day": 500
        }
    },
    "basic": {
        "tier": PlanTier.BASIC,
        "name": "Basic Plan",
        "price_monthly": 149,
        "price_yearly": 1430,  # 20% discount
        "scans_per_month": 80,
        "storage_days": 7,
        "bulk_upload_limit": 5,
        "ai_accuracy": "95%",
        "features": [
            "95_percent_accuracy",
            "gst_validation",
            "excel_csv_export",
            "priority_support",
            "7_day_storage"
        ],
        "rate_limits": {
            "api_requests_per_minute": 30,
            "api_requests_per_hour": 500,
            "api_requests_per_day": 2000
        }
    },
    "pro": {
        "tier": PlanTier.PRO,
        "name": "Pro Plan",
        "price_monthly": 299,
        "price_yearly": 2870,  # 20% discount
        "scans_per_month": 200,
        "storage_days": 30,
        "bulk_upload_limit": 10,
        "ai_accuracy": "98%",
        "features": [
            "98_percent_accuracy",
            "bulk_upload_10",
            "custom_export_templates",
            "24x7_priority_support",
            "30_day_storage",
            "advanced_gst_validation",
            "excel_csv_export"
        ],
        "rate_limits": {
            "api_requests_per_minute": 60,
            "api_requests_per_hour": 1000,
            "api_requests_per_day": 5000
        }
    },
    "ultra": {
        "tier": PlanTier.ULTRA,
        "name": "Ultra Plan",
        "price_monthly": 599,
        "price_yearly": 5750,  # 20% discount
        "scans_per_month": 500,
        "storage_days": 60,
        "bulk_upload_limit": 50,
        "ai_accuracy": "99%",
        "features": [
            "99_percent_accuracy",
            "bulk_upload_50",
            "advanced_gst_compliance",
            "dedicated_support",
            "60_day_storage",
            "custom_integrations",
            "excel_csv_export"
        ],
        "rate_limits": {
            "api_requests_per_minute": 100,
            "api_requests_per_hour": 2000,
            "api_requests_per_day": 10000
        }
    },
    "max": {
        "tier": PlanTier.MAX,
        "name": "Max Plan",
        "price_monthly": 999,
        "price_yearly": 9590,  # 20% discount
        "scans_per_month": 1000,
        "storage_days": 90,
        "bulk_upload_limit": 100,
        "ai_accuracy": "99.5%",
        "features": [
            "99_5_percent_accuracy",
            "bulk_upload_100",
            "custom_integrations",
            "24x7_priority_support",
            "90_day_storage",
            "custom_workflows",
            "excel_csv_export"
        ],
        "rate_limits": {
            "api_requests_per_minute": 200,
            "api_requests_per_hour": 5000,
            "api_requests_per_day": 20000
        }
    }
}


# Razorpay Subscription Plans (v2 - Correct Pricing)
# These map directly to plans created in Razorpay Dashboard
RAZORPAY_PLANS: Dict[str, Dict[str, Any]] = {
    "basic": {
        "razorpay_plan_id": "plan_Rat85iHwIK43DF",  # Basic Monthly ₹149
        "name": "Basic Monthly Subscription",
        "amount": 14900,  # Amount in paise (₹149.00)
        "currency": "INR",
        "interval": 1,
        "period": "monthly",
        "scans_per_month": 80
    },
    "pro": {
        "razorpay_plan_id": "plan_Rat86N89IczksF",  # Pro Monthly ₹299
        "name": "Pro Monthly Subscription",
        "amount": 29900,  # Amount in paise (₹299.00)
        "currency": "INR",
        "interval": 1,
        "period": "monthly",
        "scans_per_month": 200
    },
    "ultra": {
        "razorpay_plan_id": "plan_Rat86vgXjHOgSe",  # Ultra Monthly ₹599
        "name": "Ultra Monthly Subscription",
        "amount": 59900,  # Amount in paise (₹599.00)
        "currency": "INR",
        "interval": 1,
        "period": "monthly",
        "scans_per_month": 500
    },
    "max": {
        "razorpay_plan_id": "plan_Rat87q7Bsub6TI",  # Max Monthly ₹999
        "name": "Max Monthly Subscription",
        "amount": 99900,  # Amount in paise (₹999.00)
        "currency": "INR",
        "interval": 1,
        "period": "monthly",
        "scans_per_month": 1000
    }
}


def get_plan_config(tier: str) -> Dict[str, Any]:
    """
    Get plan configuration by tier name
    
    Args:
        tier: Plan tier name (free, basic, pro, ultra, max)
    
    Returns:
        Plan configuration dictionary
    
    Raises:
        ValueError: If tier is invalid
    """
    tier_lower = tier.lower()
    if tier_lower not in PLAN_LIMITS:
        raise ValueError(f"Invalid plan tier: {tier}. Valid tiers: {list(PLAN_LIMITS.keys())}")
    
    return PLAN_LIMITS[tier_lower]


def get_all_plans() -> Dict[str, Dict[str, Any]]:
    """Get all plan configurations"""
    return PLAN_LIMITS


def check_feature_access(tier: str, feature: str) -> bool:
    """
    Check if a plan tier has access to a specific feature
    
    Args:
        tier: Plan tier name
        feature: Feature name to check
    
    Returns:
        True if feature is available, False otherwise
    """
    try:
        plan = get_plan_config(tier)
        return feature in plan["features"]
    except ValueError:
        return False


def get_scan_limit(tier: str) -> int:
    """
    Get monthly scan limit for a plan tier
    
    Args:
        tier: Plan tier name
    
    Returns:
        Number of scans allowed per month
    """
    try:
        plan = get_plan_config(tier)
        return plan["scans_per_month"]
    except ValueError:
        return 0


def get_storage_days(tier: str) -> int:
    """
    Get storage retention days for a plan tier
    
    Args:
        tier: Plan tier name
    
    Returns:
        Number of days data is stored
    """
    try:
        plan = get_plan_config(tier)
        return plan["storage_days"]
    except ValueError:
        return 0


def get_bulk_upload_limit(tier: str) -> int:
    """
    Get bulk upload limit for a plan tier
    
    Args:
        tier: Plan tier name
    
    Returns:
        Maximum number of files that can be uploaded at once
    """
    try:
        plan = get_plan_config(tier)
        return plan["bulk_upload_limit"]
    except ValueError:
        return 1


def get_rate_limits(tier: str) -> Dict[str, int]:
    """
    Get API rate limits for a plan tier
    
    Args:
        tier: Plan tier name
    
    Returns:
        Dictionary with rate limit values
    """
    try:
        plan = get_plan_config(tier)
        return plan["rate_limits"]
    except ValueError:
        return {
            "api_requests_per_minute": 10,
            "api_requests_per_hour": 100,
            "api_requests_per_day": 500
        }


# Feature descriptions for display
FEATURE_DESCRIPTIONS = {
    "basic_ai_extraction": "Basic AI extraction with standard accuracy",
    "pdf_image_support": "Support for PDF and image files",
    "email_support": "Standard email support",
    "1_day_storage": "Invoice data stored for 1 day",
    "7_day_storage": "Invoice data stored for 7 days",
    "95_percent_accuracy": "95% AI extraction accuracy",
    "gst_validation": "GST number validation and compliance checking",
    "excel_csv_export": "Export invoices to Excel and CSV formats",
    "priority_support": "Priority email support with faster response times",
    "30_day_storage": "Invoice data stored for 30 days",
    "98_percent_accuracy": "98% AI extraction accuracy",
    "bulk_upload_20": "Upload up to 20 invoices at once",
    "custom_export_templates": "Create custom export templates",
    "24x7_priority_support": "24/7 priority support via email and chat",
    "90_day_storage": "Invoice data stored for 90 days",
    "advanced_gst_validation": "Advanced GST validation with real-time checks",
    "99_percent_accuracy": "99% AI extraction accuracy",
    "bulk_upload_50": "Upload up to 50 invoices at once",
    "api_access": "Full REST API access for integrations",
    "dedicated_support": "Dedicated support team",
    "180_day_storage": "Invoice data stored for 180 days",
    "custom_integrations": "Custom integrations with your systems",
    "99_5_percent_accuracy": "99.5% AI extraction accuracy",
    "unlimited_bulk_upload": "Unlimited bulk upload capacity",
    "dedicated_account_manager": "Dedicated account manager",
    "1_year_storage": "Invoice data stored for 1 year",
    "white_label_options": "White-label branding options",
    "custom_workflows": "Custom workflow automation"
}


def upgrade_allowed(current_tier: str, target_tier: str) -> bool:
    """
    Check if upgrade from current tier to target tier is allowed
    
    Args:
        current_tier: Current plan tier
        target_tier: Target plan tier
    
    Returns:
        True if upgrade is allowed, False otherwise
    """
    tier_hierarchy = ["free", "basic", "pro", "ultra", "max"]
    
    try:
        current_index = tier_hierarchy.index(current_tier.lower())
        target_index = tier_hierarchy.index(target_tier.lower())
        return target_index > current_index
    except ValueError:
        return False


def downgrade_allowed(current_tier: str, target_tier: str) -> bool:
    """
    Check if downgrade from current tier to target tier is allowed
    
    Args:
        current_tier: Current plan tier
        target_tier: Target plan tier
    
    Returns:
        True if downgrade is allowed, False otherwise
    """
    tier_hierarchy = ["free", "basic", "pro", "ultra", "max"]
    
    try:
        current_index = tier_hierarchy.index(current_tier.lower())
        target_index = tier_hierarchy.index(target_tier.lower())
        return target_index < current_index
    except ValueError:
        return False
