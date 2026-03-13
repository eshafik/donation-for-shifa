import asyncio
import importlib
import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvloop
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.responses import JSONResponse
from tortoise import connections
from tortoise.exceptions import DBConnectionError

from config.db import init_db, close_db, reconnect_db
from config.exceptions import tortoise_does_not_exist_handler, tortoise_integrity_error_handler
from config.renderer import (
    custom_request_validation_exception_handler,
    custom_http_exception_handler,
    custom_validation_error_handler,
)
from config.settings import TORTOISE_ORM_CONFIG, DEBUG, INSTALLED_APPS, CORS_ALLOWED_ORIGINS
from config.middleware import CustomMiddleware
from core.cache import close_redis
from tortoise.exceptions import DoesNotExist, IntegrityError

uvloop.install()


def dynamic_import(module_name: str, class_name: str):
    module = importlib.import_module(module_name)
    return getattr(module, class_name, None)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    if DEBUG:
        try:
            loop = asyncio.get_running_loop()
            print(f"Using event loop: {type(loop)}")
        except RuntimeError:
            pass
    yield
    await close_db()
    await close_redis()


app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan,
    title="FastAPI Boilerplate",
    description="Django-inspired FastAPI with Tortoise ORM, Pydantic v2, Celery, JWT auth.",
    openapi_tags=[
        {"name": "auth", "description": "Authentication (signup, token, me)"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CustomMiddleware)

# Dynamically include app routers (models are in TORTOISE_ORM_CONFIG from settings)
for app_name in INSTALLED_APPS:
    router = dynamic_import(f"{app_name}.routes", "router")
    if router:
        app.include_router(router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        conn = connections.get("default")
        await conn.execute_query("SELECT 1")
        response = await call_next(request)
        return response
    except DBConnectionError:
        await reconnect_db()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc):
    return await custom_request_validation_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return await custom_http_exception_handler(request, exc)


@app.exception_handler(ValidationError)
async def validator_error_handler(request, exc):
    return await custom_validation_error_handler(request, exc)


app.add_exception_handler(DoesNotExist, tortoise_does_not_exist_handler)
app.add_exception_handler(IntegrityError, tortoise_integrity_error_handler)

_logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def custom_exception_handler(request, exc):
    # Log 500 errors to terminal so they appear in server logs
    _logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "details": str(exc),
            "status_code": 500,
            "path": str(request.url),
        },
    )
