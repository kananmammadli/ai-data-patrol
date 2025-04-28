from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db, SessionLocal
from app.core.security import verify_token
from app.models.user import User
from app.services.user_service import UserService
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get the current user from the token."""
    print("\n" + "="*50)
    print("STARTING USER RETRIEVAL")
    print("="*50)
    print(f"Token received in get_current_user: {token}")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
            print(f"Token after removing 'Bearer ' prefix: {token}")
            
        print("\nVerifying token...")
        user_id = verify_token(token)
        if user_id is None:
            print("\nERROR: Token verification failed")
            print("="*50 + "\n")
            raise credentials_exception
            
        print(f"\nToken verified successfully!")
        print(f"User ID from token: {user_id}")
        
        print("\nLooking up user in database...")
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        if user is None:
            print(f"\nERROR: User not found for ID: {user_id}")
            print("="*50 + "\n")
            raise credentials_exception
            
        print(f"\nUser found successfully!")
        print(f"User email: {user.email}")
        print(f"User ID: {user.id}")
        print("="*50 + "\n")
        return user
    except Exception as e:
        print("\n" + "="*50)
        print("ERROR DURING USER RETRIEVAL")
        print("="*50)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("="*50 + "\n")
        raise credentials_exception 