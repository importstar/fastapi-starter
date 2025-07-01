"""
User repository for data access operations
"""

from typing import Optional
from datetime import datetime, timezone

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
        existing_user = await self.find_one({"username": user_data.username})
        if existing_user:
            raise ValueError("Username already exists")

        # Check if email already exists (if provided)
        if user_data.email:
            existing_email = await self.find_one({"email": user_data.email})
            if existing_email:
                raise ValueError("Email already exists")

        # Hash the password using the User model's method

        # Create new user instance with hashed_password
        new_user = User(
            username=user_data.username,
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
            hashed_password=generate_password_hash(
                user_data.password
            ),  # Hash the password
            is_active=True,  # Set to True by default for new registrations
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),  # Set current time for creation
        )

        # Save the user to database
        return await new_user.insert()

    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        return await self.find_one({"username": username})

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        return await self.find_one({"email": email})

    # TODO: Add your custom repository methods here
    # Example:
    # async def find_by_custom_field(self, field_value: str) -> Optional[User]:
    #     """Find user by custom field"""
    #     return await self.model.find_one({"custom_field": field_value})
