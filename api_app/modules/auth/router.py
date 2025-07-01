"""
Auth API router with REST endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...models.user_model import User
from .use_case import get_auth_use_case, AuthUseCase
from .schemas import AuthRequest, AuthResponse


router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.get("/token")
def get_token():
    return {"access_token": "your_access_token"}


# TODO: Add your API endpoints here
# Example:
# @router.get("", response_model=List[AuthResponse])
# async def list_auth(
#     auth_use_case: AuthUseCase = Depends(get_auth_use_case)
# ):
#     """List auth items"""
#     # Implement your logic here
#     pass
