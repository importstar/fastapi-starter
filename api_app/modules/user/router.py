"""
User API router with REST endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params

from api_app.core.exceptions import BusinessLogicError, DuplicatedError, ValidationError

from .use_case import get_user_use_case, UserUseCase
from .schemas import CreateUser, GetUser, UserResponse

router = APIRouter(
    prefix="/v1/user",
    tags=["User"],
)


@router.get("/", dependencies=[Depends(Params)], response_model=Page[UserResponse])
async def get_user_list(
    use_case: UserUseCase = Depends(get_user_use_case), params: GetUser = Depends()
):
    """
    Get a list of users.
    This endpoint retrieves paginated list of users with filtering.
    """
    # Convert GetUser to filters dict
    filters = params.model_dump(exclude_none=True)

    # ✅ ใช้ base get_list method ที่ return Page[UserResponse] เสมอ
    return await use_case.get_list(filters=filters if filters else None, sort=[("created_at", -1)])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def register_user(
    user_data: CreateUser, use_case: UserUseCase = Depends(get_user_use_case)
) -> UserResponse:
    """
    Register a new user.
    This endpoint handles user registration with business logic validation.
    """
    try:
        # ✅ ใช้ method ใหม่ที่ return UserResponse
        return await use_case.register_user_as_response(user_data)
    except (DuplicatedError, BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str, use_case: UserUseCase = Depends(get_user_use_case)
):
    """
    Get user by ID.
    This endpoint retrieves a user by their unique identifier.
    """
    # ✅ ใช้ method ใหม่ที่ return UserResponse
    user_response = await use_case.get_user_by_id_as_response(user_id)
    if not user_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_response


# TODO: Implement patch endpoint
# @router.patch("/{user_id}", response_model=UserResponse)
# async def update_user(
#    user_id: str,
#    user_data: dict,
#    use_case: UserUseCase = Depends(get_user_use_case)
# ):
#    pass
