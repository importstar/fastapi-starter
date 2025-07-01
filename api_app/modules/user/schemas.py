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


class UserResponse(BaseSchema, BaseUser):
    """Response schema for user operations"""

    @classmethod
    def from_entity(cls, entity) -> "UserResponse":
        """Convert entity to response schema"""
        return cls(
            id=str(entity.id),
            # TODO: Map entity fields to response fields
        )
