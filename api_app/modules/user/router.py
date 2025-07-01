"""
User API router with REST endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status

from .use_case import get_user_use_case, UserUseCase
from .schemas import CreateUser, UserResponse


router = APIRouter(prefix="/v1/user", tags=["User"])


@router.get("/")
async def get_user_list():
    """
    Get a list of users.
    This is a placeholder endpoint for listing users.
    """
    # In a real application, you would implement logic to retrieve users from the database
    return {"message": "List of users", "users": []}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: CreateUser, use_case: UserUseCase = Depends(get_user_use_case)
) -> UserResponse:
    """
    Register a new user.

    This endpoint handles user registration with business logic validation.
    """
    new_user = await use_case.register_user(user_data)
    return new_user


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: str, use_case: UserUseCase = Depends(get_user_use_case)
) -> UserResponse:
    """
    Get user by ID.

    This endpoint retrieves a user by their unique identifier.
    """
    user = await use_case.user_repository.find_one({"_id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
