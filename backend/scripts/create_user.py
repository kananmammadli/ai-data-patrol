import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User, UserRole, AuthProvider
from app.core.security import get_password_hash

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Get existing user or create new one
    user = db.query(User).filter(User.email == "admin@datapatrol.ai").first()
    
    if user:
        print("\nUpdating existing user...")
        user.hashed_password = get_password_hash("mega-suer")
    else:
        print("\nCreating new user...")
        user = User(
            id="e64430a8-e899-462e-9ee4-a3192e5120df",
            email="admin@datapatrol.ai",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            auth_provider=AuthProvider.PASSWORD,
            hashed_password=get_password_hash("mega-suer")
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    
    print(f"\nUser {'updated' if user else 'created'} successfully:")
    print(f"Email: {user.email}")
    print(f"ID: {user.id}")
    print(f"Role: {user.role}")
    print(f"Auth Provider: {user.auth_provider}")
    print(f"Is Active: {user.is_active}")
    print(f"Is Verified: {user.is_verified}")
    print(f"Has Password: {'Yes' if user.hashed_password else 'No'}")
    print(f"Password Hash: {user.hashed_password}")
    
except Exception as e:
    print(f"\nError: {str(e)}")
    db.rollback()
    
finally:
    db.close() 