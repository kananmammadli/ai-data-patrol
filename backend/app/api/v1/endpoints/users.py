from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from ....database import get_db
from ....models import UserRole
from ....schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from ....services.user_service import UserService

router = APIRouter()

@router.get("/users/", response_model=UserListResponse)
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get a list of users with optional filtering."""
    user_service = UserService(db)
    users, total = user_service.get_users(skip=skip, limit=limit, role=role, is_active=is_active)
    return UserListResponse(
        users=users,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Get a user by ID."""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    user_service = UserService(db)
    try:
        return user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Update a user."""
    user_service = UserService(db)
    try:
        return user_service.update_user(user_id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """Delete a user."""
    user_service = UserService(db)
    try:
        user_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/users/{user_id}/role", response_model=UserResponse)
def change_user_role(user_id: UUID, new_role: UserRole, db: Session = Depends(get_db)):
    """Change a user's role."""
    user_service = UserService(db)
    try:
        return user_service.change_user_role(user_id, new_role)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/users/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(user_id: UUID, db: Session = Depends(get_db)):
    """Deactivate a user."""
    user_service = UserService(db)
    try:
        return user_service.deactivate_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/users/{user_id}/activate", response_model=UserResponse)
def activate_user(user_id: UUID, db: Session = Depends(get_db)):
    """Activate a user."""
    user_service = UserService(db)
    try:
        return user_service.activate_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 