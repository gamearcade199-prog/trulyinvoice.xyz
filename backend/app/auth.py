"""
Authentication Utilities
Simple helpers for authentication with Supabase
"""
from fastapi import Depends, HTTPException, status, Header
from typing import Optional


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract user ID from Authorization header.
    
    In a Supabase setup, the frontend sends the JWT token in the Authorization header.
    For simplicity, we're extracting the user_id directly.
    
    In production, you should verify the JWT token with Supabase's public key.
    
    Args:
        authorization: Bearer token from header
        
    Returns:
        user_id: Supabase user ID
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        # Extract token from "Bearer <token>"
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization format. Expected 'Bearer <token>'"
            )
        
        token = authorization.replace("Bearer ", "")
        
        # TODO: In production, verify JWT token with Supabase
        # For now, we'll assume the token is valid
        # The frontend uses Supabase auth, which manages the session
        
        # For development/testing, you can extract user_id from the token
        # or use a mock user_id
        
        # Simple validation - just check token exists
        if not token or len(token) < 20:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # In a real implementation, decode and verify the JWT here
        # For now, return a placeholder that the frontend will handle
        return token  # Return token as user identifier for now
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Optional authentication - returns None if not authenticated.
    Use for endpoints that work for both authenticated and anonymous users.
    """
    if not authorization:
        return None
    
    try:
        return get_current_user(authorization)
    except:
        return None
