from datetime import date
from typing import Optional

from fastapi import Depends, HTTPException, Query
from tortoise.exceptions import DoesNotExist, IntegrityError

from apps.donation.schemas import (
    DonationAdminResponse,
    DonationCreate,
    DonationPublicResponse,
    DonationUpdate,
)
from apps.donation.services import (
    create_donation,
    delete_donation,
    get_donation_by_id,
    get_donations_admin,
    get_donations_public,
    update_donation,
)
from apps.user.models import User
from core.auth import get_admin_user
from core.dependencies import pagination_params


async def list_donations_public(pagination: tuple = Depends(pagination_params)):
    page, size = pagination
    result = await get_donations_public(page, size)
    result["data"] = [DonationPublicResponse.model_validate(d).model_dump(mode="json") for d in result["data"]]
    return result


async def list_donations_admin(
    pagination: tuple = Depends(pagination_params),
    search:    Optional[str]  = Query(None, description="Search donor name or transaction number"),
    date_from: Optional[date] = Query(None, description="Filter by date received from (YYYY-MM-DD)"),
    date_to:   Optional[date] = Query(None, description="Filter by date received to (YYYY-MM-DD)"),
    user:      User           = Depends(get_admin_user),
):
    page, size = pagination
    result = await get_donations_admin(page, size, search, date_from, date_to)
    result["data"] = [DonationAdminResponse.model_validate(d).model_dump(mode="json") for d in result["data"]]
    return result


async def create_donation_view(
    data: DonationCreate,
    user: User = Depends(get_admin_user),
):
    try:
        donation = await create_donation(data.model_dump(), user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Transaction number already exists")
    return {
        "message": "Donation created",
        "data": DonationAdminResponse.model_validate(donation).model_dump(mode="json"),
    }


async def get_donation_view(
    donation_id: int,
    user: User = Depends(get_admin_user),
):
    try:
        donation = await get_donation_by_id(donation_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Donation not found")
    return {"data": DonationAdminResponse.model_validate(donation).model_dump(mode="json")}


async def update_donation_view(
    donation_id: int,
    data: DonationUpdate,
    user: User = Depends(get_admin_user),
):
    update_data = data.model_dump(exclude_unset=True)
    try:
        donation = await update_donation(donation_id, update_data)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Donation not found")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Transaction number already exists")
    return {
        "message": "Donation updated",
        "data": DonationAdminResponse.model_validate(donation).model_dump(mode="json"),
    }


async def delete_donation_view(
    donation_id: int,
    user: User = Depends(get_admin_user),
):
    try:
        await delete_donation(donation_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Donation not found")
    return {"message": "Donation deleted"}
