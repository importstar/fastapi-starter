"""
Base repository pattern implementation
"""

from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from beanie import Document
from datetime import datetime
from pydantic import BaseModel


T = TypeVar("T", bound=Document)


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""

    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, entity: T) -> T:
        """Create a new entity"""
        return await entity.insert()

    async def find_by_id(self, entity_id: str) -> Optional[T]:
        """Find entity by ID"""
        try:
            return await self.model.get(entity_id)
        except Exception:
            return None

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Find all entities with pagination"""
        return await self.model.find_all().skip(skip).limit(limit).to_list()

    async def find_one(self, filters: Dict[str, Any]) -> Optional[T]:
        """Find one entity by filters"""
        return await self.model.find_one(filters)

    async def find_many(
        self, filters: Dict[str, Any], skip: int = 0, limit: int = 100
    ) -> List[T]:
        """Find multiple entities by filters"""
        return await self.model.find(filters).skip(skip).limit(limit).to_list()

    async def update(self, entity_id: str, update_data: Dict[str, Any]) -> Optional[T]:
        """Update entity by ID"""
        entity = await self.find_by_id(entity_id)
        if not entity:
            return None

        # Add timestamp
        update_data["updated_at"] = datetime.utcnow()

        # Update fields
        for key, value in update_data.items():
            setattr(entity, key, value)

        await entity.save()
        return entity

    async def delete(self, entity_id: str) -> bool:
        """Delete entity by ID"""
        entity = await self.find_by_id(entity_id)
        if not entity:
            return False

        await entity.delete()
        return True

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities"""
        if filters:
            return await self.model.find(filters).count()
        return await self.model.find_all().count()

    async def exists(self, filters: Dict[str, Any]) -> bool:
        """Check if entity exists"""
        entity = await self.find_one(filters)
        return entity is not None

    def schema_dump(
        self, schema: BaseModel, exclude: Optional[List[str]] = None, **extra_fields
    ) -> T:
        """Create entity from Pydantic schema with extra fields"""
        exclude = exclude or []
        data = schema.model_dump(exclude=set(exclude))
        data.update(extra_fields)
        return self.model(**data)
