"""
Plan Limits Configuration
DEPRECATED: Use app.config.plans instead
This file is kept for backward compatibility
"""

# Import from the main plans configuration
from ..config.plans import PLAN_LIMITS, get_scan_limit, get_plan_config

# Legacy PLAN_LIMITS for backward compatibility
# This maintains the old structure for existing code
LEGACY_PLAN_LIMITS = {
    'Free': {
        'scans': 10,
    },
    'Basic': {
        'scans': 80,
    },
    'Pro': {
        'scans': 200,
    },
    'Ultra': {
        'scans': 500,
    },
    'Max': {
        'scans': 1000,
    },
}

# Use the new PLAN_LIMITS but keep legacy structure for compatibility
PLAN_LIMITS = LEGACY_PLAN_LIMITS
