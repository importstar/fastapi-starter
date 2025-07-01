"""
Base schemas for the application
"""

from beanie import PydanticObjectId, Document
from pydantic import BaseModel, Field
from datetime import UTC, datetime
from typing import Optional, TypeVar, Type, Union


T = TypeVar("T", bound="BaseSchema")


class BaseSchema(BaseModel):
    id: Optional[Union[PydanticObjectId, str]] = Field(default=None)
    """Base schema with common response fields"""

    @classmethod
    def from_model(cls: Type[T], model: Document) -> T:
        """Create schema from Beanie model with alias support"""
        model_data = model.model_dump()
        if hasattr(model, "id") and model.id:
            model_data["id"] = str(model.id)

        schema_data = {}
        for field_name, field_info in cls.model_fields.items():
            alias = field_info.alias or field_name
            value = model_data.get(field_name, model_data.get(alias))
            if value is not None:
                schema_data[alias] = value

        return cls(**schema_data)


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
