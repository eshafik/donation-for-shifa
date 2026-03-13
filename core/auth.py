"""JWT auth: get_current_user dependency and optional get_current_user_optional."""
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status

from apps.user.models import User
from apps.user.services import get_user_by_username
from utils.jwt import verify_jwt_token


async def get_current_user(request: Request) -> User:
    """Extract Bearer token, verify JWT, load user; set request.state.user and return user. Raise 401 if invalid/missing."""
    # Prefer user set by middleware (if JWT was valid)
    if hasattr(request.state, "user") and request.state.user is not None:
        return request.state.user

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header.split(" ", 1)[1]
    sub = verify_jwt_token(token)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_username(sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    request.state.user = user
    return user


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    """Require current user to be an admin. Raises 403 if not."""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


async def get_current_user_optional(request: Request) -> Optional[User]:
    """Return current user if valid JWT present; otherwise None (for public endpoints that show extra data when logged in)."""
    if hasattr(request.state, "user"):
        return request.state.user
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    sub = verify_jwt_token(token)
    if not sub:
        return None
    user = await get_user_by_username(sub)
    if user:
        request.state.user = user
    return user
