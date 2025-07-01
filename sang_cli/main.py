"""
Main CLI application for FastAPI Beanie Starter
"""

import typer
from .create_module import app as create_module_app

app = typer.Typer(
    name="fastapi-cli", help="FastAPI Beanie Starter CLI Tools", add_completion=False
)

# Add subcommands
app.add_typer(create_module_app, name="module")


def main():
    """Main entry point for the CLI"""
    app()


if __name__ == "__main__":
    main()
