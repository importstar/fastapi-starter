"""
User use case containing business logic
"""

from fastapi import Depends

from api_app_new.models.user_model import User
from .repository import UserRepository
from .schemas import CreateUser, UserRole


class UserUseCase:
    """Use case for User business operations"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: CreateUser) -> User:
        """Register a new user with business logic validation"""
        # 1. Validate business rules
        await self._validate_user_registration(user_data)

        # 2. Process registration through repository
        try:
            new_user = await self.user_repository.register_user(user_data)
            return new_user
        except ValueError as e:
            # Convert repository errors to appropriate use case errors
            raise ValueError(f"Registration failed: {str(e)}")

    async def _validate_user_registration(self, user_data: CreateUser) -> None:
        """Validate business rules for user registration"""
        # Example business rules validation:

        # 1. Username format validation
        if len(user_data.username) < 3:
            raise ValueError("Username must be at least 3 characters long")

        # 2. Password strength validation
        if len(user_data.password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if user_data.password != user_data.confirm_password:
            raise ValueError("Password and confirm password do not match")

        # 3. Email format validation (if provided)
        if user_data.email and "@" not in user_data.email:
            raise ValueError("Invalid email format")

        # 4. Role validation
        if user_data.role not in UserRole:
            raise ValueError(
                f"Invalid role. Must be one of: {', '.join(UserRole.__members__.keys())}"
            )

    async def _post_registration_actions(self, user: User) -> None:
        """Perform actions after successful user registration"""
        # TODO: Add post-registration business logic
        # Examples:
        # - Send welcome email
        # - Log registration event
        # - Create user profile
        # - Set up default preferences
        pass

    # TODO: Add your additional business logic methods here


# Dependency providers
async def get_user_repository() -> UserRepository:
    """Get user repository instance"""
    return UserRepository()


async def get_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> UserUseCase:
    """Get user use case with injected dependencies"""
    return UserUseCase(user_repository=repository)
