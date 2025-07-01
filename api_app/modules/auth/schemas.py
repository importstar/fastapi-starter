"""
Auth module schemas (DTOs)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from ...core.base_schemas import BaseSchema


class AuthRequest(BaseModel):
    """Request schema for auth operations"""
    # TODO: Add your request fields here
    pass


class AuthResponse(BaseSchema):
    """Response schema for auth operations"""
    id: str
    # TODO: Add your response fields here

    @classmethod
    def from_entity(cls, entity) -> "AuthResponse":
        """Convert entity to response schema"""
        return cls(
            id=str(entity.id),
            # TODO: Map entity fields to response fields
        )
