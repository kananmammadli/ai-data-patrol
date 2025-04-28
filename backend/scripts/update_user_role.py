from app.db.session import SessionLocal
from app.services.user_service import UserService
from app.models import UserRole

def update_user_role(email: str, new_role: UserRole):
    db = SessionLocal()
    try:
        user_service = UserService(db)
        user = user_service.get_user_by_email(email)
        if not user:
            print(f"User with email {email} not found")
            return
        
        print(f"Found user: {user.email} with current role: {user.role}")
        updated_user = user_service.change_user_role(user.id, new_role)
        print(f"Updated user role to: {updated_user.role}")
    finally:
        db.close()

if __name__ == "__main__":
    email = "kanan.mammadli+datapatrol@gmail.com"
    update_user_role(email, UserRole.ADMIN) 