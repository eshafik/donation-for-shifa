from apps.donation.services import get_stats_cached


async def stats_summary_view():
    stats = await get_stats_cached()
    return {"data": stats}
