"""
Base schemas for the application
"""

from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from datetime import UTC, datetime
from typing import Optional


class BaseSchema(BaseModel):
    id: Optional[PydanticObjectId | str] = Field(default=None)
    """Base schema with common response fields"""
    pass


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""

    created_at: datetime
    updated_at: Optional[datetime] = None


class ErrorResponse(BaseModel):
    """Standard error response"""

    detail: str
    code: Optional[str] = None
    timestamp: datetime = lambda: datetime.now(UTC)


class SuccessResponse(BaseModel):
    """Standard success response"""

    message: str
    data: Optional[dict] = None
