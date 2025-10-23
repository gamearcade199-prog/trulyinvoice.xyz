"""
Authentication Utilities - Production Grade
Secure JWT validation with Supabase integration
"""
from fastapi import Depends, HTTPException, status, Header, Request
from typing import Optional, Dict
from datetime import datetime
import os
import logging
from functools import wraps

# Set up logger
logger = logging.getLogger(__name__)

# Import Supabase for JWT validation
from app.services.supabase_helper import supabase


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract and validate user ID from Authorization header.
    Validates JWT token with Supabase Auth.
    
    Args:
        authorization: Authorization header (Bearer {token})
    
    Returns:
        Authenticated user ID (UUID)
    
    Raises:
        HTTPException: 401 if token is invalid or missing
        HTTPException: 403 if token is expired
    
    Example:
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    if not authorization:
        logger.warning("❌ Missing authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        logger.debug(f"📋 Authorization header received: {authorization[:50]}...")
        # Expected format: "Bearer {jwt_token}"
        parts = authorization.split()
        if len(parts) != 2:
            logger.warning(f"❌ Invalid header format: {len(parts)} parts")
            raise ValueError("Invalid header format")
        
        scheme, token = parts
        logger.debug(f"   Scheme: {scheme}, Token length: {len(token)}")
        
        if scheme.lower() != "bearer":
            logger.warning(f"❌ Invalid scheme: {scheme}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme. Use: 'Bearer {token}'",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        logger.debug(f"🔐 Validating token with Supabase Auth...")
        # Validate token with Supabase Auth
        try:
            logger.debug(f"   Calling supabase.auth.get_user()...")
            response = supabase.auth.get_user(token)
            logger.debug(f"   Response type: {type(response)}")
            logger.debug(f"   Response object: {response}")
            
            # Handle response - check for user
            user = None
            if hasattr(response, 'user'):
                user = response.user
                logger.debug(f"   Found user attribute: {user}")
            elif isinstance(response, dict) and 'user' in response:
                user = response.get('user')
                logger.debug(f"   Found user in dict: {user}")
            else:
                logger.debug(f"   Response has no user attribute/key")
            
            if not user:
                logger.warning("❌ Token validation failed: No user in response")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired authentication token"
                )
            
            # Extract user ID
            user_id = None
            if hasattr(user, 'id'):
                user_id = user.id
                logger.debug(f"   User ID from attribute: {user_id}")
            elif isinstance(user, dict) and 'id' in user:
                user_id = user.get('id')
                logger.debug(f"   User ID from dict: {user_id}")
            
            if not user_id:
                logger.warning("❌ Could not extract user ID from response")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired authentication token"
                )
            
            logger.info(f"✅ User authenticated: {user_id}")
            return user_id
            
        except HTTPException:
            raise
        except AttributeError as e:
            logger.error(f"❌ Response structure error: {str(e)}")
            logger.error(f"   Response: {response}")
            logger.error(f"   Response dir: {dir(response) if response else 'None'}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to parse token response"
            )
        except Exception as e:
            logger.warning(f"⚠️ Token validation error: {str(e)}")
            logger.warning(f"   Error type: {type(e).__name__}")
            import traceback
            logger.debug(f"   Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to validate authentication token: {str(e)}"
            )
        
    except ValueError:
        logger.warning("❌ Invalid authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected: 'Bearer {token}'"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Optional authentication - returns None if not authenticated.
    Use for endpoints that work for both authenticated and anonymous users.
    
    Args:
        authorization: Optional authorization header
    
    Returns:
        User ID if authenticated, None otherwise
    """
    if not authorization:
        return None
    
    try:
        return get_current_user(authorization)
    except HTTPException:
        return None
    except Exception:
        return None


def verify_user_ownership(user_id: str, resource_owner_id: str) -> bool:
    """
    Verify that a user owns a specific resource.
    
    Args:
        user_id: ID of the user making the request
        resource_owner_id: ID of the resource owner
    
    Returns:
        True if user owns the resource, raises HTTPException otherwise
    
    Raises:
        HTTPException: 403 if user doesn't own the resource
    """
    if user_id != resource_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    return True
