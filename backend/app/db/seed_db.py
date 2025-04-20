import os
import sys
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from passlib.context import CryptContext

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import User, UserRole, AuthProvider

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def seed_database():
    """Seed the database with initial data."""
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@datapatrol.io").first()
        if not admin_user:
            # Create admin user with password
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # In production, use a secure password
            admin_user = User(
                email="admin@datapatrol.io",
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN,
                password_hash=get_password_hash(admin_password),
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Created admin user")

        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    load_dotenv()
    seed_database() 