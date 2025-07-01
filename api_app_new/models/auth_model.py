"""
Auth Beanie document model
"""
from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime


class Auth(Document):
    """
    Auth document model for MongoDB collection
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "auth"  # Collection name in MongoDB
        indexes = [
            "name",
            "status",
            "created_at"
        ]

    def __str__(self) -> str:
        return f"Auth(name={self.name}, status={self.status})"
