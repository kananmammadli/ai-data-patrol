from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
            
        print(f"Verifying token: {token[:10]}...")  # Log first 10 chars for security
        
        # Decode token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        print(f"Token payload: {payload}")
        
        # Check expiration
        exp = payload.get("exp")
        if exp is None:
            print("No expiration time in token")
            return None
            
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            print("Token has expired")
            return None
            
        # Get user ID
        user_id = payload.get("sub")
        if not user_id:
            print("No user ID in token")
            return None
            
        print(f"Token verified successfully for user: {user_id}")
        return str(user_id)
        
    except JWTError as e:
        print(f"Token verification failed: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error during token verification: {str(e)}")
        return None 