from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import status

from ....database import get_db
from ....models import UserRole, User, AuthProvider
from ....schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from ....services.user_service import UserService
from ....api.deps import get_current_user

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get the current user's information."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

@router.get("/users/", response_model=UserListResponse)
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a list of users with optional filtering."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
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

@router.post("/{user_id}/auth-provider", response_model=UserResponse)
def update_user_auth_provider(
    user_id: UUID,
    auth_provider: AuthProvider,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Update a user's authentication provider."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user_service = UserService(db)
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user_service.update_user_auth_provider(user.email, auth_provider)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/users/{user_id}/password", response_model=UserResponse)
def update_user_password(
    user_id: UUID,
    password_data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Update a user's password."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user_service = UserService(db)
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        password = password_data.get("password")
        if not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required"
            )
        user_service.update_user_password(user.email, password)
        return user_service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 