"""
Auth use case containing business logic
"""

from fastapi import Depends, HTTPException, status
from typing import List, Optional

from api_app_new.core.exceptions import ValidationError
from api_app_new.models.auth_model import Auth
from .repository import AuthRepository
from .schemas import AuthRequest, AuthResponse


class AuthUseCase:
    """Use case for Auth business operations"""

    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def create(self, data: AuthRequest) -> Auth:
        """Create new auth"""
        # 1. Validate business rules
        await self._validate_unique_name(data.name)

        # 2. Create entity
        auth_data = data.model_dump()
        auth_data["status"] = "active"

        new_auth = Auth(**auth_data)

        # 3. Save to repository
        result = await self.auth_repository.create(new_auth)
        return result

    async def get_all(self) -> List[Auth]:
        """Get all active auth items"""
        return await self.auth_repository.find_active()

    async def get_by_id(self, auth_id: str) -> Optional[Auth]:
        """Get auth by ID"""
        return await self.auth_repository.find_by_id(auth_id)

    async def update(self, auth_id: str, data: AuthRequest) -> Optional[Auth]:
        """Update auth"""
        # 1. Check if exists
        existing_auth = await self.get_by_id(auth_id)
        if not existing_auth:
            return None

        # 2. Validate unique name (if changed)
        if data.name != existing_auth.name:
            await self._validate_unique_name(data.name)

        # 3. Update
        update_data = data.model_dump(exclude_unset=True)
        return await self.auth_repository.update(auth_id, update_data)

    async def delete(self, auth_id: str) -> bool:
        """Soft delete auth"""
        return await self.auth_repository.update(auth_id, {"status": "deleted"})

    async def _validate_unique_name(self, name: str) -> None:
        """Validate that auth name is unique"""
        existing = await self.auth_repository.find_by_name(name)
        if existing:
            raise ValidationError(f"Auth with name '{name}' already exists")


# Dependency providers
async def get_auth_repository() -> AuthRepository:
    """Get auth repository instance"""
    return AuthRepository()


async def get_auth_use_case(
    repository: AuthRepository = Depends(get_auth_repository),
) -> AuthUseCase:
    """Get auth use case with injected dependencies"""
    return AuthUseCase(auth_repository=repository)
