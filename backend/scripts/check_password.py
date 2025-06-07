import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.core.config import settings

# Create engine and session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Get admin user
    user = db.query(User).filter(User.email == "admin@datapatrol.ai").first()
    
    if user:
        print("\nAdmin user found:")
        print(f"Email: {user.email}")
        print(f"ID: {user.id}")
        print(f"Role: {user.role}")
        print(f"Auth Provider: {user.auth_provider}")
        print(f"Is Active: {user.is_active}")
        print(f"Is Verified: {user.is_verified}")
        print(f"Has Password: {'Yes' if user.hashed_password else 'No'}")
        print(f"Password Hash: {user.hashed_password}")
    else:
        print("\nAdmin user not found!")
    
except Exception as e:
    print(f"\nError: {str(e)}")
    db.rollback()
    
finally:
    db.close() 