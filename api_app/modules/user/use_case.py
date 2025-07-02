"""
User use case containing business logic
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi_pagination import Page
from werkzeug.security import generate_password_hash
from fastapi import Depends

from .model import User
from .repository import UserRepository, get_user_repository
from .schemas import CreateUser, UserResponse  # เพิ่ม UserResponse
from ...core.base_use_case import BaseUseCase
from ...core.exceptions import ValidationError, DuplicatedError, BusinessLogicError


class UserUseCase(BaseUseCase[User, UserRepository, UserResponse]):
    """Use case for User business operations"""

    def __init__(self, repository: UserRepository):
        super().__init__(repository, UserResponse)

    async def register_user(self, user_data: CreateUser) -> User:
        """Register a new user with complete business logic"""

        # Business validation: Check username uniqueness
        existing_user = await self.repository.find_by_username(user_data.username)
        if existing_user:
            raise DuplicatedError("Username already exists")

        # Business validation: Check email uniqueness (if provided)
        if user_data.email:
            existing_email = await self.repository.find_by_email(user_data.email)
            if existing_email:
                raise DuplicatedError("Email already exists")

        # Business logic: Hash password
        hashed_password = generate_password_hash(user_data.password)

        # Business logic: Set default values and timestamps
        user_dict = user_data.model_dump(exclude={"password", "confirm_password"})
        user_dict.update(
            {
                "hashed_password": hashed_password,
                "is_active": True,
                "role": "user",  # Default role
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            }
        )
        try:
            user = User(**user_dict)
            new_user = await self.repository.create(user)
            return new_user
        except Exception as e:
            raise ValidationError(f"Registration failed: {str(e)}")

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user - business logic"""
        from werkzeug.security import check_password_hash

        # Find user
        user = await self.repository.find_by_username(username)
        if not user:
            return None

        # Business rule: Check if user is active
        if not user.is_active:
            raise BusinessLogicError("Account is deactivated")

        # Verify password
        if not check_password_hash(user.hashed_password, password):
            return None

        # Business logic: Update last login
        await self.repository.update(
            str(user.id), {"last_login": datetime.now(timezone.utc)}
        )

        return user

    async def deactivate_user(self, user_id: str, admin_user_id: str) -> User:
        """Deactivate user - with business rules"""

        # Business validation: Check admin permissions
        admin = await self.repository.find_by_id(admin_user_id)
        if not admin or admin.role not in ["admin", "super_admin"]:
            raise BusinessLogicError("Only admins can deactivate users")

        # Get target user
        user = await self.repository.find_by_id(user_id)
        if not user:
            raise BusinessLogicError("User not found")

        # Business rule: Cannot deactivate super admin
        if user.role == "super_admin":
            raise BusinessLogicError("Cannot deactivate super admin")

        # Business rule: Cannot deactivate yourself
        if user_id == admin_user_id:
            raise BusinessLogicError("Cannot deactivate yourself")

        # Update through repository
        return await self.repository.update(
            user_id,
            {
                "is_active": False,
                "deactivated_by": admin_user_id,
                "deactivated_at": datetime.now(timezone.utc),
            },
        )

    async def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> bool:
        """Change password with business validation"""
        from werkzeug.security import check_password_hash

        # Get user
        user = await self.repository.find_by_id(user_id)
        if not user:
            raise BusinessLogicError("User not found")

        # Business validation: Verify old password
        if not check_password_hash(user.hashed_password, old_password):
            raise BusinessLogicError("Invalid current password")

        # Business rule: Password strength
        if len(new_password) < 8:
            raise BusinessLogicError("New password must be at least 8 characters")

        # Business rule: Cannot use same password
        if check_password_hash(user.hashed_password, new_password):
            raise BusinessLogicError(
                "New password must be different from current password"
            )

        # Hash new password and update
        hashed_password = generate_password_hash(new_password)
        await self.repository.update(
            user_id,
            {
                "hashed_password": hashed_password,
                "password_changed_at": datetime.now(timezone.utc),
            },
        )

        return True

    async def get_user_profile(self, user_id: str) -> Optional[User]:
        """Get user profile with linked data"""
        return await self.repository.find_by_id(user_id, fetch_links=True)

    async def search_users(
        self,
        query: str,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Page[User]:
        """Search users with business logic"""
        from beanie.operators import And, Or

        # Business validation
        if len(query.strip()) < 2:
            raise BusinessLogicError("Search query must be at least 2 characters")

        # Build query filters
        filters = []

        # Search in username, email, or full_name
        search_filter = Or(
            User.username.regex(query, "i"),
            User.email.regex(query, "i"),
            (
                User.full_name.regex(query, "i")
                if hasattr(User, "full_name")
                else User.username.regex(query, "i")
            ),
        )
        filters.append(search_filter)

        # Additional filters
        if role:
            filters.append(User.role == role)

        if is_active is not None:
            filters.append(User.is_active == is_active)

        # Combine filters
        combined_filters = And(*filters) if len(filters) > 1 else filters[0]

        return await self.repository.find_many(
            filters=combined_filters, sort=[("created_at", -1)]
        )

    async def get_user_by_id_as_response(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID as UserResponse schema"""
        user = await self.get_by_id(user_id)
        if user:
            return UserResponse.model_validate(user.model_dump())
        return None

    async def register_user_as_response(self, user_data: CreateUser) -> UserResponse:
        """Register user and return as UserResponse"""
        user = await self.register_user(user_data)
        return UserResponse.model_validate(user.model_dump())


# Dependency providers
async def get_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> UserUseCase:
    """Get user use case with injected dependencies"""
    return UserUseCase(repository)
