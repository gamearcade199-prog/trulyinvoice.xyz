"""
Debug endpoint to check auth headers
"""
from fastapi import APIRouter, Header
from typing import Optional

router = APIRouter()

@router.get("/debug/auth-header")
async def debug_auth_header(authorization: Optional[str] = Header(None)):
    """
    Debug endpoint to see what auth headers are being sent
    No authentication required
    """
    return {
        "authorization_header_received": bool(authorization),
        "authorization_length": len(authorization) if authorization else 0,
        "authorization_preview": f"{authorization[:50]}..." if authorization and len(authorization) > 50 else authorization,
        "has_bearer": "bearer" in (authorization or "").lower()
    }
