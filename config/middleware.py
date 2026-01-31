# config/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from tortoise.exceptions import DoesNotExist

from apps.user.models import User
from apps.user.services import get_user_by_username
from core.cache import get_user_cached, set_user_cached
from utils.jwt import verify_jwt_token


class CustomMiddleware(BaseHTTPMiddleware):
    """JWT auth middleware: set request.state.user when valid Bearer token present."""

    async def dispatch(self, request: Request, call_next: callable) -> Response:
        request.state.custom_attribute = "Custom value"
        request.state.user = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            sub = verify_jwt_token(token)
            if sub:
                cached = await get_user_cached(sub)
                if cached is not None:
                    try:
                        user = await User.get(id=cached["id"])
                        request.state.user = user
                    except DoesNotExist:
                        pass
                else:
                    user = await get_user_by_username(sub)
                    if user:
                        request.state.user = user
                        await set_user_cached(
                            sub,
                            {"id": user.id, "username": user.username, "email": user.email, "name": user.name},
                            ttl_seconds=300,
                        )

        response = await call_next(request)
        return response
