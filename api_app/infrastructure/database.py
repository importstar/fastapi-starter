import importlib
import pkgutil
from typing import Sequence, Type, TypeVar
from inspect import getmembers, isclass
import motor.motor_asyncio
import beanie
from loguru import logger


DocumentType = TypeVar("DocumentType", bound=beanie.Document)


class BeanieClient:
    def __init__(self):
        self.client = None
        self.database = None
        self.settings = None

    def _gather_documents(self) -> Sequence[Type[DocumentType]]:
        """Returns a list of all MongoDB document models defined in `models` module."""

        documents = []
        models_module_name = "api_app.models"

        try:
            # Import the models package
            models_package = importlib.import_module(models_module_name)

            # Get all modules in the models package
            for finder, module_name, ispkg in pkgutil.iter_modules(
                models_package.__path__, models_package.__name__ + "."
            ):
                if not ispkg:  # Only process module files, not sub-packages
                    try:
                        # Import each module
                        module = importlib.import_module(module_name)

                        # Get all classes from the module
                        for name, obj in getmembers(module, isclass):
                            # Check if it's a Beanie Document and not the base Document class
                            if (
                                issubclass(obj, beanie.Document)
                                and obj.__name__ != "Document"
                                and obj.__module__ == module_name
                            ):  # Ensure it's defined in this module
                                documents.append(obj)
                                logger.info(
                                    f"Found Document model: {obj.__name__} in {module_name}"
                                )

                    except Exception as e:
                        logger.warning(f"Could not import module {module_name}: {e}")
                        continue

        except Exception as e:
            logger.error(f"Could not import models package {models_module_name}: {e}")
            return []

        if not documents:
            logger.warning("No Document models found in models package")

        return documents

    async def init_beanie(self, settings):
        """Initialize Beanie with MongoDB connection"""
        try:
            self.settings = settings
            logger.info(f"Connecting to MongoDB: {settings.DATABASE_URI}")

            # Create motor client
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                settings.DATABASE_URI, connect=True
            )

            # Get database
            self.database = self.client.get_default_database()
            logger.debug(f"Using database: {self.database.name}")

            # Gather document models dynamically
            documents = self._gather_documents()

            if not documents:
                logger.warning(
                    "No document models found, Beanie initialization skipped"
                )
                return

            logger.info(f"Initializing Beanie with {len(documents)} models:")
            for document in documents:
                logger.info(f"  - {document.__name__}")

            # Initialize Beanie
            await beanie.init_beanie(
                database=self.database,
                document_models=documents,
            )

            logger.info("Beanie initialization successful")

        except Exception as e:
            logger.error(f"Beanie initialization failed: {e}")
            raise

    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    async def ping(self) -> bool:
        """Check database connection"""
        try:
            if self.client:
                await self.client.admin.command("ping")
                return True
            return False
        except Exception as e:
            logger.error(f"Database ping failed: {e}")
            return False


# Global beanie client instance
beanie_client = BeanieClient()


async def init_beanie(settings):
    """Initialize Beanie with settings"""
    await beanie_client.init_beanie(settings)


async def close_beanie():
    """Close Beanie connection"""
    await beanie_client.close()


def get_database():
    """Get database instance"""
    return beanie_client.database
