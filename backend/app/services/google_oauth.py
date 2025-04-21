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

class GoogleOAuthService:
    def __init__(self, db: Session):
        self.db = db
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for tokens."""
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data, ssl=self.ssl_context) as response:
                if response.status != 200:
                    response_text = await response.text()
                    print(f"Token exchange failed. Status: {response.status}, Response: {response_text}")
                    raise ValueError(f"Failed to exchange code for token: {response_text}")
                
                token_data = await response.json()
                print("Token exchange successful:", token_data)
                return token_data

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
                raise ValueError('Invalid audience')

            # Verify the token's issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid issuer')

            return idinfo
        except Exception as e:
            raise ValueError(f'Invalid token: {str(e)}')

    async def get_or_create_user(self, google_user_info: dict) -> User:
        """Get or create a user based on Google user info."""
        # Print the structure for debugging
        print("Google User Info:", google_user_info)
        
        # Extract email from the response
        email = google_user_info.get('email')
        if not email:
            raise ValueError("Email not found in Google user info")
            
        user_service = UserService(self.db)
        user = user_service.get_user_by_email(email)
        
        if not user:
            # Create new user using UserCreate schema
            user_data = UserCreate(
                email=email,
                first_name=google_user_info.get('given_name', ''),
                last_name=google_user_info.get('family_name', ''),
                password=None,  # No password for OAuth users
                role=UserRole.VIEWER,  # Default role
                is_active=True,
                auth_provider=AuthProvider.GOOGLE  # Set auth provider
            )
            try:
                user = user_service.create_user(user_data)
                print("Created new user:", user)
            except Exception as e:
                print("Error creating user:", str(e))
                raise
        
        return user

def google_oauth_service(db: Session) -> GoogleOAuthService:
    return GoogleOAuthService(db) 