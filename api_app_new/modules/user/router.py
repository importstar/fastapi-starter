"""
User API router with REST endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status

from .use_case import get_user_use_case, UserUseCase
from .schemas import CreateUser


router = APIRouter(prefix="/v1/user", tags=["User"])


@router.get("/")
async def get_user_list():
    """
    Get a list of users.
    This is a placeholder endpoint for listing users.
    """
    # In a real application, you would implement logic to retrieve users from the database
    return {"message": "List of users", "users": []}


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: CreateUser, use_case: UserUseCase = Depends(get_user_use_case)
):
    """
    Register a new user.

    This endpoint handles user registration with business logic validation.
    """
    new_user = await use_case.register_user(user_data)
    return {
        "message": "User registered successfully",
        "user_id": str(new_user.id),
        "username": new_user.username,
    }
