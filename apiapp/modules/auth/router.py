"""
Auth API router - authentication endpoints
"""

import typing

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

from .use_case import AuthUseCase, get_auth_use_case
from . import schemas
from ...core import exceptions


router = APIRouter(prefix="/v1/auth", tags=["Authentication"])


@router.post("/token", summary="Get OAuth2 access token")
async def login_for_access_token(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> schemas.GetAccessTokenResponse:
    """Get access token using username and password."""
    return await use_case.login_for_access_token(form_data)


@router.post("/login")
async def login(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> schemas.Token:
    """Login and get access + refresh tokens."""
    return await use_case.authenticate(form_data)


@router.get("/refresh_token")
async def refresh_token(
    credentials: typing.Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
    use_case: AuthUseCase = Depends(get_auth_use_case),
) -> schemas.GetAccessTokenResponse:
    """Refresh access token using refresh token."""
    return await use_case.refresh_token(credentials)
