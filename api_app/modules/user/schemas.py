"""
User module schemas (DTOs)
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

from ...core.base_schemas import BaseSchema


class UserRole(Enum):
    """Enumeration for user roles"""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class BaseUser(BaseModel):
    """Base schema with common fields for user"""

    username: str = Field(
        ..., min_length=1, max_length=50, description="Username of the user"
    )
    name: str = Field(..., min_length=1, max_length=100, description="Name of the user")
    email: Optional[str] = Field(
        default=None, max_length=255, description="Email address of the user"
    )
    role: UserRole = Field(
        default=UserRole.USER, description="List of roles assigned to the user"
    )
    is_active: bool = Field(default=True, description="Indicates if the user is active")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation timestamp",
    )


class CreateUser(BaseModel):
    username: str = Field(
        ..., min_length=1, max_length=50, description="Username of the user"
    )
    name: str = Field(..., min_length=1, max_length=100, description="Name of the user")
    email: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Email address of the user",
        examples=["user@email.com"],
    )
    password: str = Field(
        ..., min_length=8, max_length=128, description="User password"
    )
    role: str = Field(
        default=UserRole.USER.value, description="Role assigned to the user"
    )
    confirm_password: str = Field(
        ..., min_length=8, max_length=128, description="Confirm user password"
    )


class UserParams(BaseSchema):
    username: Optional[str] = Field(
        default=None, description="Filter by username", max_length=50
    )
    email: Optional[str] = Field(
        default=None, description="Filter by email", max_length=255
    )
    role: Optional[UserRole] = Field(default=None, description="Filter by user role")
    is_active: Optional[bool] = Field(
        default=None, description="Filter by active status"
    )


class UserResponse(BaseSchema, BaseUser):
    name: str = Field(description="Full name of the user", alias="fullname")
