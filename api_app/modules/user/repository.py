"""
User repository for data access operations
"""

from typing import Optional
from datetime import datetime, timezone

from api_app.core.exceptions import DuplicatedError

from ...core.base_repository import BaseRepository
from ...models.user_model import User
from .schemas import CreateUser
from werkzeug.security import generate_password_hash


class UserRepository(BaseRepository[User]):
    """Repository for User data operations"""

    def __init__(self):
        super().__init__(User)

    async def register_user(self, user_data: CreateUser) -> User:
        """Register a new user with CreateUser schema"""
        # Check if username already exists
        # existing_user = await self.find_one({"username": user_data.username})
        # if existing_user:
        #     raise DuplicatedError("Username already exists")

        # # Check if email already exists (if provided)
        # if user_data.email:
        #     existing_email = await self.find_one({"email": user_data.email})
        #     if existing_email:
        #         raise DuplicatedError("Email already exists")

        # Hash the password using the User model's method

        # Create new user instance using schema_dump with extra fields
        new_user = self.schema_dump(
            user_data,
            exclude=["password"],
            hashed_password=generate_password_hash(user_data.password),
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        await new_user.save()

    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        return await self.find_one({"username": username})

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        return await self.find_one({"email": email})
