"""
Base use case pattern implementation
"""

from typing import TypeVar, Optional, Dict, Any, Generic, Union
from abc import ABC
from beanie import Document
from fastapi_pagination import Page
from pydantic import BaseModel

from .base_repository import BaseRepository
from .exceptions import ValidationError, BusinessLogicError


T = TypeVar("T", bound=Document)
R = TypeVar("R", bound=BaseRepository)
S = TypeVar("S", bound=BaseModel)  # Schema type


class BaseUseCase(ABC, Generic[T, R]):
    """Simple base use case for business logic"""

    def __init__(self, repository: R):
        self.repository = repository

    # CRUD Operations
    async def create(self, data: Union[BaseModel, Dict[str, Any]]) -> T:
        """Create a new entity"""
        try:
            # Convert schema to dict if needed
            create_data = data.model_dump() if isinstance(data, BaseModel) else data
            entity = await self.repository.create(create_data)
            return entity
        except Exception as e:
            raise BusinessLogicError(f"Creation failed: {str(e)}")

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID"""
        return await self.repository.find_by_id(entity_id)

    async def get_all(
        self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 100
    ) -> Page[T]:
        """Get all entities"""
        if filters:
            return await self.repository.find_many(filters, skip, limit)
        return await self.repository.find_all(skip, limit)

    async def update(
        self, entity_id: str, data: Union[BaseModel, Dict[str, Any]]
    ) -> Optional[T]:
        """Update entity"""
        existing = await self.repository.find_by_id(entity_id)
        if not existing:
            return None

        try:
            # Convert schema to dict if needed
            update_data = data.model_dump() if isinstance(data, BaseModel) else data
            updated = await self.repository.update(entity_id, update_data)
            return updated
        except Exception as e:
            raise BusinessLogicError(f"Update failed: {str(e)}")

    async def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        existing = await self.repository.find_by_id(entity_id)
        if not existing:
            return False

        try:
            success = await self.repository.delete(entity_id)
            return success
        except Exception as e:
            raise BusinessLogicError(f"Deletion failed: {str(e)}")

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities"""
        return await self.repository.count(filters)

    async def exists(self, filters: Dict[str, Any]) -> bool:
        """Check if entity exists"""
        return await self.repository.exists(filters)

    # Utility methods
    def _raise_validation_error(self, message: str, field: Optional[str] = None):
        """Raise validation error"""
        raise ValidationError(message, field=field)

    def _raise_business_error(self, message: str, code: Optional[str] = None):
        """Raise business logic error"""
        raise BusinessLogicError(message, code=code)
