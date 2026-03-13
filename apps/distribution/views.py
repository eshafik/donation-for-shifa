from datetime import date
from typing import Optional

from fastapi import Depends, HTTPException, Query
from tortoise.exceptions import DoesNotExist

from apps.distribution.schemas import (
    DistributionAdminResponse,
    DistributionCreate,
    DistributionPublicResponse,
    DistributionUpdate,
)
from apps.distribution.services import (
    create_distribution,
    delete_distribution,
    get_distribution_by_id,
    get_distributions_admin,
    get_distributions_public,
    update_distribution,
)
from apps.user.models import User
from core.auth import get_admin_user
from core.dependencies import pagination_params


async def list_distributions_public(pagination: tuple = Depends(pagination_params)):
    page, size = pagination
    result = await get_distributions_public(page, size)
    result["data"] = [DistributionPublicResponse.model_validate(d).model_dump(mode="json") for d in result["data"]]
    return result


async def list_distributions_admin(
    pagination: tuple = Depends(pagination_params),
    search:    Optional[str]  = Query(None, description="Search recipient name or address"),
    date_from: Optional[date] = Query(None, description="Filter by date distributed from (YYYY-MM-DD)"),
    date_to:   Optional[date] = Query(None, description="Filter by date distributed to (YYYY-MM-DD)"),
    user:      User           = Depends(get_admin_user),
):
    page, size = pagination
    result = await get_distributions_admin(page, size, search, date_from, date_to)
    result["data"] = [DistributionAdminResponse.model_validate(d).model_dump(mode="json") for d in result["data"]]
    return result


async def create_distribution_view(
    data: DistributionCreate,
    user: User = Depends(get_admin_user),
):
    distribution = await create_distribution(data.model_dump(), user)
    return {
        "message": "Distribution created",
        "data": DistributionAdminResponse.model_validate(distribution).model_dump(mode="json"),
    }


async def get_distribution_view(
    distribution_id: int,
    user: User = Depends(get_admin_user),
):
    try:
        distribution = await get_distribution_by_id(distribution_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Distribution not found")
    return {"data": DistributionAdminResponse.model_validate(distribution).model_dump(mode="json")}


async def update_distribution_view(
    distribution_id: int,
    data: DistributionUpdate,
    user: User = Depends(get_admin_user),
):
    update_data = data.model_dump(exclude_unset=True)
    try:
        distribution = await update_distribution(distribution_id, update_data)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Distribution not found")
    return {
        "message": "Distribution updated",
        "data": DistributionAdminResponse.model_validate(distribution).model_dump(mode="json"),
    }


async def delete_distribution_view(
    distribution_id: int,
    user: User = Depends(get_admin_user),
):
    try:
        await delete_distribution(distribution_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Distribution not found")
    return {"message": "Distribution deleted"}
