from fastapi import APIRouter

from utils.response_wrapper import response_wrapper
from .views import stats_summary_view

router = APIRouter(tags=["stats"])

router.get(
    "/api/v1/stats/summary",
    summary="Get donation and distribution summary stats",
    responses={200: {"description": "Stats summary"}},
)(response_wrapper(stats_summary_view))
