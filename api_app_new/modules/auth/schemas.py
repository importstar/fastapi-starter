"""
Auth module schemas (DTOs)
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from api_app_new.core.schemas import BaseSchema


class BaseAuth(BaseModel):
    """Base schema with common fields"""

    name: str = Field(..., min_length=1, max_length=100, description="Name of the auth")
    description: Optional[str] = Field(None, max_length=500, description="Description")


class CreateAuth(BaseAuth):
    """Request schema for creating auth"""

    pass


class UpdateAuth(BaseAuth):
    """Request schema for updating auth"""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the auth")
    description: Optional[str] = Field(None, max_length=500, description="Description")


class GetAuth(BaseAuth, BaseSchema):
    """Response schema with additional fields"""

    id: str
    status: str = "active"
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, entity) -> "GetAuth":
        """Convert entity to response schema"""
        return cls(
            id=str(entity.id),
            name=entity.name,
            description=entity.description,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
