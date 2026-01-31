from fastapi import APIRouter
from utils.response_wrapper import response_wrapper
from core.auth import get_current_user
from .views import sign_up, get_token, me
from .schemas import UserResponse, TokenResponse

router = APIRouter(prefix="/api/v1/user", tags=["user"])

router.post(
    "/signup",
    summary="Register a new user",
    responses={200: {"description": "Returns access_token and token_type"}},
)(response_wrapper(sign_up))
router.post(
    "/token",
    summary="Obtain JWT access token",
    responses={200: {"description": "Returns access_token and token_type"}, 401: {"description": "Invalid credentials"}},
)(response_wrapper(get_token))
router.get(
    "/me",
    response_model=UserResponse,
    summary="Current user profile",
    responses={401: {"description": "Not authenticated"}},
)(me)
