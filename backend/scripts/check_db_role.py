import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models import User

def check_db_role():
    db = SessionLocal()
    try:
        # Query for both email addresses
        users = db.query(User).filter(
            User.email.in_(['kanan.mammadli+datapatrol@gmail.com', 'kanan.mammadli@gmail.com'])
        ).all()
        
        for user in users:
            print(f"User email: {user.email}")
            print(f"User role: {user.role}")
            print(f"User ID: {user.id}")
            print(f"Auth provider: {user.auth_provider}")
            print("-" * 50)
    finally:
        db.close()

if __name__ == "__main__":
    check_db_role() 