from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from app.utils import http_error, validation_error
from contextlib import asynccontextmanager
from app import middlewares, routes
from app.core.app_settings import AppSettings, get_app_settings


def create_app() -> FastAPI:
    settings: AppSettings = get_app_settings()
    settings.configure_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await routes.init_router(app, settings=settings)
        yield

    app = FastAPI(**settings.fastapi_kwargs)
    app.add_exception_handler(HTTPException, http_error.http_error_handler)
    app.add_exception_handler(
        RequestValidationError, validation_error.http422_error_handler
    )
    middlewares.init_middleware(app, settings=settings)
    app.router.lifespan_context = lifespan

    @app.get("/health", tags=["health"])
    async def health():
        return {"message": "service is working"}

    return app
