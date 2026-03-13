from datetime import date
from typing import Any, Dict, Optional

from tortoise.expressions import Q

from apps.distribution.models import DonationDistribution
from apps.user.models import User
from utils.pagination import paginate


async def get_distributions_public(page: int, size: int) -> Dict[str, Any]:
    return await paginate(DonationDistribution.all(), page, size)


async def get_distributions_admin(
    page: int,
    size: int,
    search: Optional[str],
    date_from: Optional[date],
    date_to: Optional[date],
) -> Dict[str, Any]:
    qs = DonationDistribution.all()
    if search:
        qs = qs.filter(Q(recipient_name__icontains=search) | Q(address__icontains=search))
    if date_from:
        qs = qs.filter(date_distributed__gte=date_from)
    if date_to:
        qs = qs.filter(date_distributed__lte=date_to)
    return await paginate(qs, page, size)


async def get_distribution_by_id(distribution_id: int) -> DonationDistribution:
    return await DonationDistribution.get(id=distribution_id)


async def create_distribution(data: dict, user: User) -> DonationDistribution:
    dist = await DonationDistribution.create(**data, created_by=user)
    return await DonationDistribution.get(id=dist.id)


async def update_distribution(distribution_id: int, data: dict) -> DonationDistribution:
    distribution = await DonationDistribution.get(id=distribution_id)
    for key, value in data.items():
        setattr(distribution, key, value)
    await distribution.save()
    return await DonationDistribution.get(id=distribution_id)


async def delete_distribution(distribution_id: int) -> None:
    distribution = await DonationDistribution.get(id=distribution_id)
    await distribution.delete()
