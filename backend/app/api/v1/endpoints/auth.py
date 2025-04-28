from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.token import Token
from app.schemas.user import UserCreate, User as UserSchema, UserLogin, PasswordUpdate, PasswordResetRequest, PasswordResetConfirm
from app.services.google_oauth import google_oauth_service
from app.core.security import create_access_token, verify_password, get_password_hash, verify_token
from app.models.user import User, AuthProvider
from typing import Any, Dict
import os
from datetime import timedelta
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Login with email and password.
    """
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not user.verify_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active"
        )
    
    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "token_type": "bearer"
    }

@router.post("/password/update")
async def update_password(
    password_data: PasswordUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update user password.
    """
    if not current_user.verify_password(password_data.current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    current_user.set_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}

@router.post("/password/reset-request", response_model=Dict[str, str])
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    """Request a password reset."""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Don't reveal whether a user exists
        return {"message": "If an account exists with this email, a password reset link has been sent"}

    # Create a reset token
    token_data = {"sub": str(user.id)}
    token = create_access_token(token_data)
    
    # In development, return the token directly
    if os.getenv("ENVIRONMENT", "development") == "development":
        return {"message": "Development mode: use this token", "token": token}
    
    # In production, send the token via email
    return {"message": "If an account exists with this email, a password reset link has been sent"}

@router.post("/password/reset", response_model=Dict[str, str])
async def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    """Reset password using reset token."""
    try:
        # Verify the token and get user ID
        user_id = verify_token(request.token)
        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Invalid token"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        # Update password and auth provider
        user.hashed_password = get_password_hash(request.new_password)
        user.auth_provider = AuthProvider.PASSWORD
        db.commit()
        
        return {"message": "Password reset successful"}
    except Exception as e:
        print("Error in password reset:", str(e))
        print("Error type:", type(e).__name__)
        print("Error args:", e.args)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/google")
async def google_auth(request: Request):
    """
    Get Google OAuth URL.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth client ID not configured"
        )
        
    # Remove trailing slash from base_url if it exists
    base_url = str(request.base_url).rstrip('/')
    redirect_uri = f"{base_url}/api/v1/auth/google/callback"
    scope = "openid email profile"
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    
    return {"auth_url": auth_url}

@router.get("/google/callback")
async def google_callback(
    code: str,
    request: Request,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Handle Google OAuth callback.
    """
    try:
        # Exchange code for token
        base_url = str(request.base_url).rstrip('/')
        redirect_uri = f"{base_url}/api/v1/auth/google/callback"
        print("Using redirect URI:", redirect_uri)
        
        token_response = await google_oauth_service(db).exchange_code_for_token(
            code,
            redirect_uri
        )
        
        if not token_response.get("id_token"):
            print("No ID token received from Google")
            raise ValueError("No ID token received from Google")
            
        # Get user info from token
        user_info = await google_oauth_service(db).verify_token(token_response["id_token"])
        print("Verified user info:", {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "email_verified": user_info.get("email_verified")
        })
        
        # Get or create user
        user = await google_oauth_service(db).get_or_create_user(user_info)
        print("User created/retrieved:", {
            "id": str(user.id),
            "email": user.email,
            "auth_provider": user.auth_provider
        })
        
        # Create access token with longer expiration
        access_token = create_access_token(
            {"sub": str(user.id)},
            expires_delta=timedelta(days=7)  # Token expires in 7 days
        )
        print("Created access token for user:", str(user.id))
        
        # Redirect to frontend with token
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        redirect_url = f"{frontend_url}/auth/callback?token={access_token}"
        print("Redirecting to:", redirect_url)
        
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        print("Error in Google callback:", str(e))
        print("Error type:", type(e).__name__)
        print("Error args:", e.args)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/register", response_model=Dict[str, str])
async def register_user(
    user_data: UserLogin,
    db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    """Register a new user with password authentication."""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user_service = UserService(db)
        user = user_service.create_password_user(user_data.email, user_data.password)
        
        return {"message": "User registered successfully"}
    except Exception as e:
        print("Error in register_user:", str(e))
        print("Error type:", type(e).__name__)
        print("Error args:", e.args)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/password/update-direct", response_model=Dict[str, str])
async def update_password_direct(
    email: str,
    new_password: str,
    db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    """Update a user's password directly (development only)."""
    if os.getenv("ENVIRONMENT", "development") != "development":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in development mode"
        )
    
    try:
        user_service = UserService(db)
        user_service.update_user_password(email, new_password)
        return {"message": "Password updated successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print("Error in update_password_direct:", str(e))
        print("Error type:", type(e).__name__)
        print("Error args:", e.args)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 