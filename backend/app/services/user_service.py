from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from ..models import User, UserRole
from ..schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from uuid import UUID

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[User], int]:
        """Get a list of users with optional filtering."""
        query = select(User)
        
        if role is not None:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Get total count
        count_query = select(func.count()).select_from(User)
        if role is not None:
            count_query = count_query.filter(User.role == role)
        if is_active is not None:
            count_query = count_query.filter(User.is_active == is_active)
        total = self.db.scalar(count_query)
        
        # Apply pagination
        users = self.db.scalars(query.offset(skip).limit(limit)).all()
        
        return users, total

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        if self.get_user_by_email(user_data.email):
            raise ValueError("User with this email already exists")
        
        # Create new user
        db_user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
            password_hash=get_password_hash(user_data.password),
            is_active=user_data.is_active
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user

    def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        """Update a user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise ValueError("User not found")
        
        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user

    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise ValueError("User not found")
        
        self.db.delete(db_user)
        self.db.commit()
        
        return True

    def change_user_role(self, user_id: UUID, new_role: UserRole) -> User:
        """Change a user's role."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise ValueError("User not found")
        
        db_user.role = new_role
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user

    def deactivate_user(self, user_id: UUID) -> User:
        """Deactivate a user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise ValueError("User not found")
        
        db_user.is_active = False
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user

    def activate_user(self, user_id: UUID) -> User:
        """Activate a user."""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise ValueError("User not found")
        
        db_user.is_active = True
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user 