from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.token import Token
from app.schemas.user import UserCreate, User as UserSchema, UserLogin
from app.services.google_oauth import google_oauth_service
from app.core.security import create_access_token, verify_password
from app.models.user import User
from typing import Any
import os

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
    if not user or not verify_password(user_data.password, user.password_hash):
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

@router.get("/google")
async def google_auth(request: Request):
    """
    Redirect to Google OAuth consent screen.
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
    
    return RedirectResponse(url=auth_url)

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
            raise ValueError("No ID token received from Google")
            
        # Get user info from token
        user_info = await google_oauth_service(db).verify_token(token_response["id_token"])
        print("Verified user info:", user_info)
        
        # Get or create user
        user = await google_oauth_service(db).get_or_create_user(user_info)
        print("User created/retrieved:", user)
        
        # Create access token
        access_token = create_access_token({"sub": str(user.id)})
        print("Created access token")
        
        # Redirect to frontend with token
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
        redirect_url = f"{frontend_url}/auth/callback?token={access_token}"
        print("Redirecting to:", redirect_url)
        
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        print("Error in Google callback:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) 