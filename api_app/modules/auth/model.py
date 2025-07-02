"""
Auth Beanie document model
"""
from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone


class Auth(Document):
    """
    Auth document model for MongoDB collection
    """
    # TODO: Add your model fields here
    # Example:
    # name: str = Field(..., min_length=1, max_length=100)
    # description: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "auth"  # Collection name in MongoDB
        # TODO: Add your indexes here
        # indexes = [
        #     "field_name",
        #     "created_at"
        # ]

    def __str__(self) -> str:
        return f"Auth(id={self.id})"
