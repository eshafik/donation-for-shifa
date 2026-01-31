"""Centralized exception handlers for ORM and validation errors."""
from fastapi import Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError


async def tortoise_does_not_exist_handler(request: Request, exc: DoesNotExist) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "success": False},
    )


async def tortoise_integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Conflict: resource already exists or constraint violated", "success": False},
    )
