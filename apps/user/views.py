from fastapi import Depends, HTTPException

from apps.user.models import User
from apps.user.schemas import UserCreate, UserCred, UserResponse
from apps.user.services import create_user, authenticate_user
from core.auth import get_current_user
from utils.jwt import generate_jwt_token


async def sign_up(data: UserCreate):
    data = data.model_dump()
    user = await create_user(**data)
    token = generate_jwt_token(user=user)
    return {"access_token": token, "token_type": "bearer"}


async def get_token(data: UserCred):
    data = data.model_dump()
    user = await authenticate_user(**data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = generate_jwt_token(user=user)
    return {"access_token": token, "token_type": "bearer"}


async def me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user)
