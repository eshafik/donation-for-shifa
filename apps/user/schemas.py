from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserCred(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response (access_token, token_type)."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Response schema for User; ORM-backed with from_attributes."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[str] = None
    name: Optional[str] = None
    joined_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Exclude password and other sensitive fields by not declaring them
