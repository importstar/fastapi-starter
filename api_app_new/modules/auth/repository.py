"""
Auth repository for data access operations
"""

from typing import List, Optional

from api_app_new.core.base_repository import BaseRepository
from api_app_new.models.auth_model import Auth


class AuthRepository(BaseRepository[Auth]):
    """Repository for Auth data operations"""

    def __init__(self):
        super().__init__(Auth)

    async def find_by_name(self, name: str) -> Optional[Auth]:
        """Find auth by name"""
        return await self.model.find_one({"name": name})

    async def find_active(self) -> List[Auth]:
        """Find only active auth records"""
        return await self.model.find({"status": "active"}).to_list()

    async def find_by_status(self, status: str) -> List[Auth]:
        """Find auth by status"""
        return await self.model.find({"status": status}).to_list()
