import json
from datetime import date
from decimal import Decimal
from typing import Any, Dict, Optional

from tortoise.expressions import Q
from tortoise.functions import Sum

from apps.donation.models import Donation
from apps.user.models import User
from core.cache import get_redis
from utils.pagination import paginate


async def get_donations_public(page: int, size: int) -> Dict[str, Any]:
    return await paginate(Donation.all(), page, size)


async def get_donations_admin(
    page: int,
    size: int,
    search: Optional[str],
    date_from: Optional[date],
    date_to: Optional[date],
) -> Dict[str, Any]:
    qs = Donation.all()
    if search:
        qs = qs.filter(Q(donor_name__icontains=search) | Q(transaction_number__icontains=search))
    if date_from:
        qs = qs.filter(date_received__gte=date_from)
    if date_to:
        qs = qs.filter(date_received__lte=date_to)
    return await paginate(qs, page, size)


async def get_donation_by_id(donation_id: int) -> Donation:
    return await Donation.get(id=donation_id)


async def create_donation(data: dict, user: User) -> Donation:
    d = await Donation.create(**data, created_by=user)
    return await Donation.get(id=d.id)


async def update_donation(donation_id: int, data: dict) -> Donation:
    donation = await Donation.get(id=donation_id)
    for key, value in data.items():
        setattr(donation, key, value)
    await donation.save()
    return await Donation.get(id=donation_id)


async def delete_donation(donation_id: int) -> None:
    donation = await Donation.get(id=donation_id)
    await donation.delete()


async def get_stats_cached() -> Dict[str, Any]:
    """Return total collected and distributed stats. Cached in Redis for 60s."""
    redis = get_redis()
    cache_key = "stats:summary"

    if redis:
        try:
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception:
            redis = None  # Redis unavailable; fall through to DB query

    # Lazy import to avoid circular dependency (distribution app created in Phase 3)
    from apps.distribution.models import DonationDistribution

    donation_agg     = await Donation.all().annotate(total=Sum("amount")).values("total")
    distribution_agg = await DonationDistribution.all().annotate(total=Sum("amount_received")).values("total")

    total_collected   = donation_agg[0]["total"]     or Decimal("0.00")
    total_distributed = distribution_agg[0]["total"] or Decimal("0.00")

    stats = {
        "total_collected":   f"{total_collected:.2f}",
        "total_distributed": f"{total_distributed:.2f}",
        "donation_count":    await Donation.all().count(),
        "distribution_count": await DonationDistribution.all().count(),
    }

    if redis:
        try:
            await redis.set(cache_key, json.dumps(stats), ex=60)
        except Exception:
            pass

    return stats
