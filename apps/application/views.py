from typing import Optional

from fastapi import Depends, HTTPException, Request
from tortoise.exceptions import DoesNotExist

from apps.application.schemas import (
    ApplicationAdminResponse,
    ApplicationCreate,
    ApplicationStatusUpdate,
    ApplicationSubmitResponse,
)
from apps.application.services import (
    create_application,
    get_application_by_id,
    get_applications_admin,
    update_application_status,
)
from apps.user.models import User
from core.auth import get_admin_user
from utils.rate_limiter import check_ip_rate_limit


async def submit_application_view(
    request: Request,
    data: ApplicationCreate,
    _: None = Depends(check_ip_rate_limit),
):
    application = await create_application(data.model_dump())
    return {
        "message": "Application submitted",
        "data": ApplicationSubmitResponse.model_validate(application).model_dump(mode="json"),
    }


async def list_applications_admin(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None,
    user: User = Depends(get_admin_user),
):
    result = await get_applications_admin(page, size, search, status)
    result["data"] = [
        ApplicationAdminResponse.model_validate(a).model_dump(mode="json")
        for a in result["data"]
    ]
    return result


async def get_application_view(
    application_id: int,
    user: User = Depends(get_admin_user),
):
    try:
        application = await get_application_by_id(application_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "message": "Success",
        "data": ApplicationAdminResponse.model_validate(application).model_dump(mode="json"),
    }


async def update_application_status_view(
    application_id: int,
    data: ApplicationStatusUpdate,
    user: User = Depends(get_admin_user),
):
    try:
        application = await update_application_status(
            application_id, data.status, data.admin_notes, user
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "message": "Application status updated",
        "data": ApplicationAdminResponse.model_validate(application).model_dump(mode="json"),
    }
