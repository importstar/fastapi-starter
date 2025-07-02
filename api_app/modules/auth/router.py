"""
Auth API router with REST endpoints
"""

from fastapi import APIRouter


router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.get("/token")
def get_token():
    return {"access_token": "your_access_token"}
