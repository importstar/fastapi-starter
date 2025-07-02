"""
User repository for data access operations
"""

from typing import Optional
from ...core.base_repository import BaseRepository
from .model import User


class UserRepository(BaseRepository[User]):
    """Repository for User data operations - Data access only"""

    def __init__(self):
        super().__init__(User)

    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        return await self.find_one({"username": username})

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        return await self.find_one({"email": email})

    # สืบทอดจาก BaseRepository:
    # - find_by_id, find_many, update, delete ฯลฯ


# Dependency providers
async def get_user_repository() -> UserRepository:
    """Get user repository instance"""
    return UserRepository()
