"""
CLI script to create a new FastAPI module following the project structure.
"""

import typer
from pathlib import Path
import re
from typing import Optional

app = typer.Typer(
    name="create-module",
    help="Create a new FastAPI module skeleton following Clean Architecture patterns",
    add_completion=False,
)


def validate_feature_name(feature_name: str) -> bool:
    """Validate feature name format (lowercase, alphanumeric, underscores)"""
    return bool(re.match(r"^[a-z][a-z0-9_]*$", feature_name))


def create_directory_structure(base_path: Path, feature_name: str) -> Path:
    """Create the module directory structure"""
    module_path = base_path / "api_app" / "modules" / feature_name
    module_path.mkdir(parents=True, exist_ok=True)
    return module_path


def create_init_file(module_path: Path):
    """Create __init__.py file"""
    init_content = '"""Module initialization"""'
    (module_path / "__init__.py").write_text(init_content)


def create_schemas_file(module_path: Path, feature_name: str):
    """Create schemas.py file"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))

    content = f'''"""
{pascal_case} module schemas (DTOs)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from ...core.base_schemas import BaseSchema


class {pascal_case}Request(BaseModel):
    """Request schema for {feature_name} operations"""
    # TODO: Add your request fields here
    pass


class {pascal_case}Response(BaseSchema):
    """Response schema for {feature_name} operations"""
    id: str
    # TODO: Add your response fields here

    @classmethod
    def from_entity(cls, entity) -> "{pascal_case}Response":
        """Convert entity to response schema"""
        return cls(
            id=str(entity.id),
            # TODO: Map entity fields to response fields
        )
'''

    (module_path / "schemas.py").write_text(content)


def create_repository_file(module_path: Path, feature_name: str):
    """Create repository.py file"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))

    content = f'''"""
{pascal_case} repository for data access operations
"""
from typing import List, Optional

from ...core.base_repository import BaseRepository
from ...models.{feature_name}_model import {pascal_case}


class {pascal_case}Repository(BaseRepository[{pascal_case}]):
    """Repository for {pascal_case} data operations"""
    
    def __init__(self):
        super().__init__({pascal_case})

    # TODO: Add your custom repository methods here
    # Example:
    # async def find_by_custom_field(self, field_value: str) -> Optional[{pascal_case}]:
    #     """Find {feature_name} by custom field"""
    #     return await self.model.find_one({{"custom_field": field_value}})
'''

    (module_path / "repository.py").write_text(content)


def create_use_case_file(module_path: Path, feature_name: str):
    """Create use_case.py file"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))

    content = f'''"""
{pascal_case} use case containing business logic
"""
from fastapi import Depends
from typing import List, Optional

from ...models.{feature_name}_model import {pascal_case}
from .repository import {pascal_case}Repository
from .schemas import {pascal_case}Request, {pascal_case}Response


class {pascal_case}UseCase:
    """Use case for {pascal_case} business operations"""
    
    def __init__(self, {feature_name}_repository: {pascal_case}Repository):
        self.{feature_name}_repository = {feature_name}_repository

    # TODO: Add your business logic methods here
    # Example:
    # async def process_{feature_name}(self, data: {pascal_case}Request) -> {pascal_case}Response:
    #     """Process {feature_name} business logic"""
    #     # 1. Validate business rules
    #     # 2. Process data
    #     # 3. Call repository
    #     # 4. Return result
    #     pass


# Dependency providers
async def get_{feature_name}_repository() -> {pascal_case}Repository:
    """Get {feature_name} repository instance"""
    return {pascal_case}Repository()


async def get_{feature_name}_use_case(
    repository: {pascal_case}Repository = Depends(get_{feature_name}_repository)
) -> {pascal_case}UseCase:
    """Get {feature_name} use case with injected dependencies"""
    return {pascal_case}UseCase({feature_name}_repository=repository)
'''

    (module_path / "use_case.py").write_text(content)


def create_router_file(module_path: Path, feature_name: str):
    """Create router.py file"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))

    content = f'''"""
{pascal_case} API router with REST endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...models.user_model import User
from .use_case import get_{feature_name}_use_case, {pascal_case}UseCase
from .schemas import {pascal_case}Request, {pascal_case}Response


router = APIRouter(prefix="/v1/{feature_name}", tags=["{pascal_case}"])

# TODO: Add your API endpoints here
# Example:
# @router.get("", response_model=List[{pascal_case}Response])
# async def list_{feature_name}(
#     {feature_name}_use_case: {pascal_case}UseCase = Depends(get_{feature_name}_use_case)
# ):
#     """List {feature_name} items"""
#     # Implement your logic here
#     pass
'''

    (module_path / "router.py").write_text(content)


def create_model_file(base_path: Path, feature_name: str):
    """Create model file"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))
    models_path = base_path / "api_app" / "models"
    model_file = models_path / f"{feature_name}_model.py"

    content = f'''"""
{pascal_case} Beanie document model
"""
from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone


class {pascal_case}(Document):
    """
    {pascal_case} document model for MongoDB collection
    """
    # TODO: Add your model fields here
    # Example:
    # name: str = Field(..., min_length=1, max_length=100)
    # description: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "{feature_name}"  # Collection name in MongoDB
        # TODO: Add your indexes here
        # indexes = [
        #     "field_name",
        #     "created_at"
        # ]

    def __str__(self) -> str:
        return f"{pascal_case}(id={{self.id}})"
'''

    model_file.write_text(content)
    return model_file


def print_success_message(feature_name: str, module_path: Path, model_file: Path):
    """Print success message with next steps"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))

    typer.echo("", color=True)
    typer.secho(
        f"✅ Successfully created '{feature_name}' module skeleton!",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.secho(f"📁 Module path: {module_path}", fg=typer.colors.BLUE)
    typer.secho(f"📄 Model file: {model_file}", fg=typer.colors.BLUE)
    typer.echo("")
    typer.secho("🔧 Next steps:", fg=typer.colors.YELLOW, bold=True)
    typer.echo(
        f"1. Update api_app/infrastructure/database.py to include {pascal_case} model"
    )
    typer.echo(
        "2. Customize the generated skeleton files according to your requirements:"
    )
    typer.echo(f"   - Add model fields in {feature_name}_model.py")
    typer.echo("   - Add request/response schemas in schemas.py")
    typer.echo("   - Add repository methods in repository.py")
    typer.echo("   - Add business logic in use_case.py")
    typer.echo("   - Add API endpoints in router.py")
    typer.echo("3. The router will be auto-discovered when you add endpoints")
    typer.echo("")
    typer.secho("📝 Generated skeleton files:", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"   - {module_path}/__init__.py")
    typer.echo(f"   - {module_path}/schemas.py (basic structure)")
    typer.echo(f"   - {module_path}/repository.py (basic structure)")
    typer.echo(f"   - {module_path}/use_case.py (basic structure)")
    typer.echo(f"   - {module_path}/router.py (basic structure)")
    typer.echo(f"   - {model_file} (basic structure)")
    typer.echo("")
    typer.secho(
        "💡 All files contain TODO comments to guide your implementation",
        fg=typer.colors.MAGENTA,
    )


@app.command()
def add(
    feature_name: Optional[str] = typer.Argument(
        None, help="Feature name (e.g., 'products', 'orders', 'user_profiles')"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force creation even if module already exists"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be created without actually creating files",
    ),
):
    """
    Create a new FastAPI module skeleton following Clean Architecture patterns.

    Generates basic structure without CRUD implementation - ready for customization.
    """

    # Get current directory
    current_dir = Path.cwd()

    # Check if we're in the right directory
    if not (current_dir / "api_app").exists():
        typer.secho(
            "❌ Error: This script must be run from the project root directory",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            "   Make sure you're in the directory containing 'api_app' folder",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    # Get feature name from user if not provided
    if not feature_name:
        feature_name = (
            typer.prompt(
                "📝 Enter feature name (e.g., 'products', 'orders', 'user_profiles')"
            )
            .strip()
            .lower()
        )

    if not feature_name:
        typer.secho("❌ Feature name cannot be empty", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    if not validate_feature_name(feature_name):
        typer.secho(
            "❌ Invalid feature name. Use lowercase letters, numbers, and underscores only.",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            "   Examples: 'products', 'user_profiles', 'order_items'",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(1)

    # Check if module already exists
    module_path = current_dir / "api_app" / "modules" / feature_name
    if module_path.exists() and not force:
        typer.secho(
            f"❌ Module '{feature_name}' already exists at {module_path}",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            "   Use --force to overwrite or choose a different name",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(1)

    # Show what will be created
    typer.secho(
        f"📋 Creating module skeleton: {feature_name}", fg=typer.colors.CYAN, bold=True
    )
    typer.secho(f"📁 Location: api_app/modules/{feature_name}", fg=typer.colors.BLUE)

    if dry_run:
        typer.secho(
            "\n🔍 DRY RUN - Files that would be created:",
            fg=typer.colors.YELLOW,
            bold=True,
        )
        typer.echo(f"   - {module_path}/__init__.py")
        typer.echo(f"   - {module_path}/schemas.py")
        typer.echo(f"   - {module_path}/repository.py")
        typer.echo(f"   - {module_path}/use_case.py")
        typer.echo(f"   - {module_path}/router.py")
        typer.echo(f"   - api_app/models/{feature_name}_model.py")
        return

    # Confirm creation if not in force mode
    if not force:
        confirm = typer.confirm(f"❓ Create '{feature_name}' module skeleton?")
        if not confirm:
            typer.secho("❌ Module creation cancelled", fg=typer.colors.RED)
            raise typer.Exit(0)

    try:
        # Create module structure
        typer.secho("\n🔨 Creating module skeleton structure...", fg=typer.colors.CYAN)
        module_path = create_directory_structure(current_dir, feature_name)

        # Create files
        typer.echo("📝 Creating __init__.py...")
        create_init_file(module_path)

        typer.echo("📝 Creating schemas.py skeleton...")
        create_schemas_file(module_path, feature_name)

        typer.echo("📝 Creating repository.py skeleton...")
        create_repository_file(module_path, feature_name)

        typer.echo("📝 Creating use_case.py skeleton...")
        create_use_case_file(module_path, feature_name)

        typer.echo("📝 Creating router.py skeleton...")
        create_router_file(module_path, feature_name)

        typer.echo("📝 Creating model skeleton...")
        model_file = create_model_file(current_dir, feature_name)

        # Success message
        print_success_message(feature_name, module_path, model_file)

    except Exception as e:
        typer.secho(f"❌ Error creating module: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@app.command()
def list():
    """List all existing modules in the project."""
    current_dir = Path.cwd()
    modules_path = current_dir / "api_app" / "modules"

    if not modules_path.exists():
        typer.secho("❌ No modules directory found", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    modules = [
        d.name
        for d in modules_path.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name != "__pycache__"
    ]

    if not modules:
        typer.secho("📭 No modules found", fg=typer.colors.YELLOW)
        return

    typer.secho("📚 Existing modules:", fg=typer.colors.CYAN, bold=True)
    for module in sorted(modules):
        typer.secho(f"   - {module}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
