"""
Auth API router with REST endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from api_app_new.core.dependencies import get_current_active_user
from api_app_new.models.user_model import User
from .use_case import get_auth_use_case, AuthUseCase
from .schemas import AuthRequest, AuthResponse


router = APIRouter(prefix="/v1/auth", tags=["Auth"])

@router.post("/login")
async def login()