from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from app.core.config import settings
from app.models.user import User, UserRole, AuthProvider
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
import aiohttp
import json
import certifi
import ssl
from typing import Dict, Any
import uuid

class GoogleOAuthService:
    def __init__(self, db: Session):
        self.db = db
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.user_service = UserService(db)

    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for tokens."""
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(token_url, data=data, ssl=self.ssl_context) as response:
                    if response.status != 200:
                        response_text = await response.text()
                        print(f"Token exchange failed. Status: {response.status}, Response: {response_text}")
                        raise ValueError(f"Failed to exchange code for token: {response_text}")
                    
                    token_data = await response.json()
                    print("Token exchange successful")
                    return token_data
        except aiohttp.ClientError as e:
            print(f"Network error during token exchange: {str(e)}")
            raise ValueError(f"Network error during token exchange: {str(e)}")
        except Exception as e:
            print(f"Unexpected error during token exchange: {str(e)}")
            raise ValueError(f"Unexpected error during token exchange: {str(e)}")

    async def verify_token(self, token: str) -> dict:
        """Verify the Google ID token and return user info."""
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.client_id
            )
            
            # Verify the token's audience
            if idinfo['aud'] != self.client_id:
                print(f"Invalid audience. Expected: {self.client_id}, Got: {idinfo['aud']}")
                raise ValueError('Invalid audience')

            # Verify the token's issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                print(f"Invalid issuer. Got: {idinfo['iss']}")
                raise ValueError('Invalid issuer')

            return idinfo
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            raise ValueError(f'Invalid token: {str(e)}')

    async def get_or_create_user(self, user_info: Dict[str, Any]) -> User:
        email = user_info.get("email")
        if not email:
            raise ValueError("No email provided in user info")

        # Check if user already exists
        user = self.user_service.get_user_by_email(email)
        if user:
            print(f"Found existing user: {email}")
            return user

        # Create new user without password
        user_data = UserCreate(
            id=str(uuid.uuid4()),  # Generate a new UUID
            email=email,
            first_name=user_info.get("given_name"),
            last_name=user_info.get("family_name"),
            is_verified=user_info.get("email_verified", False),
            auth_provider=AuthProvider.GOOGLE
        )

        print(f"Creating new user: {email}")
        user = self.user_service.create_user(user_data)
        print(f"User created: {user.email}")
        return user

def google_oauth_service(db: Session) -> GoogleOAuthService:
    return GoogleOAuthService(db) 