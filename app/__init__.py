from fastapi import FastAPI, APIRouter
from fastapi.exceptions import HTTPException, RequestValidationError
from .utils import http_error, validation_error
from contextlib import asynccontextmanager
from . import middlewares, routers
from .models import init_beanie
from loguru import logger
from .core.app_settings import AppSettings, get_app_settings
from dotenv import load_dotenv
import os


def create_app() -> FastAPI:
    env_file = ".env.dev" if os.getenv("APP_ENV") == "dev" else ".env"
    load_dotenv(env_file)
    logger.debug(os.getenv("APP_ENV"))

    settings: AppSettings = get_app_settings()
    settings.configure_logging()

    app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)
    app.add_exception_handler(HTTPException, http_error.http_error_handler)
    app.add_exception_handler(
        RequestValidationError, validation_error.http422_error_handler
    )
    middlewares.init_middleware(app, settings=settings)
    app.router.lifespan_context = lifespan

    @app.get("/health", tags=["health"])
    async def health():
        logger.debug("Health check")
        return {"ok": True}

    def use_route_names_as_operation_ids(app: FastAPI) -> None:
        """
        Simplify operation IDs so that generated API clients have simpler function
        names.

        Should be called only after all routes have been added.
        """
        for route in app.routes:
            if isinstance(route, APIRouter):
                route.operation_id = route.name

    use_route_names_as_operation_ids(app)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: AppSettings = get_app_settings()
    await routers.init_router(app, settings=settings)
    await init_beanie(app, settings)
    yield
