"""
User Beanie document model
"""

from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone


class User(Document):
    """
    User document model for MongoDB collection
    """

    username: str = Field(..., min_length=1, max_length=50, unique=True)
    name: str = Field(..., min_length=1, max_length=100)
    hashed_password: str
    email: Optional[str] = Field(None, max_length=100, unique=True)
    is_active: bool = Field(default=True, description="Indicates if the user is active")
    role: str = Field(..., description="List of roles assigned to the user")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "users"  # Collection name in MongoDB
        # TODO: Add your indexes here
        # indexes = [
        #     "field_name",
        #     "created_at"
        # ]

    def __str__(self) -> str:
        return f"User(id={self.id})"

    def set_password(self, password: str) -> None:
        """
        Set the user's password after hashing it.
        This method should be called before saving the user document.
        """
        from werkzeug.security import generate_password_hash

        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Verify the provided password against the stored hashed password.
        Returns True if the password matches, False otherwise.
        """
        from werkzeug.security import check_password_hash

        return check_password_hash(self.hashed_password, password)
