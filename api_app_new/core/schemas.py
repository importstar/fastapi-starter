"""
Base schemas for the application
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BaseSchema(BaseModel):
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
    timestamp: datetime = datetime.utcnow()


class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str
    data: Optional[dict] = None
