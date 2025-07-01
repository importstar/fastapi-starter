"""
User API router with REST endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from loguru import logger

from api_app.core.base_schemas import ErrorResponse

from .use_case import get_user_use_case, UserUseCase
from .schemas import CreateUser, UserParams, UserResponse


router = APIRouter(
    prefix="/v1/user",
    tags=["User"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "User Not Found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)


@router.get("/", dependencies=[Depends(Params)])
async def get_user_list(
    use_case: UserUseCase = Depends(get_user_use_case), params: UserParams = Depends()
) -> Page[UserResponse]:
    """
    Get a list of users.
    This endpoint retrieves paginated list of users with filtering.
    """
    # Convert UserParams to filters dict
    filters = params.model_dump(exclude_none=True)

    # Get users from use case
    users = await use_case.get_all(filters=filters if filters else None)

    # Convert each user model to UserResponse schema
    user_responses = [UserResponse.from_model(user) for user in users]

    # Return paginated response
    # Note: You might need to implement proper pagination in your use_case.get_all()
    return Page(
        items=user_responses,
        total=len(user_responses),
        page=1,
        size=len(user_responses),
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: CreateUser, use_case: UserUseCase = Depends(get_user_use_case)
) -> UserResponse:
    """
    Register a new user.

    This endpoint handles user registration with business logic validation.
    """
    new_user = await use_case.register_user(user_data)
    return UserResponse.from_model(new_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str, use_case: UserUseCase = Depends(get_user_use_case)
):
    """
    Get user by ID.

    This endpoint retrieves a user by their unique identifier.
    """
    user = await use_case.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponse.from_model(user)
