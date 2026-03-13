from fastapi import APIRouter

from utils.response_wrapper import response_wrapper
from .views import (
    get_application_view,
    list_applications_admin,
    submit_application_view,
    update_application_status_view,
)

router = APIRouter(tags=["application"])

# Public
router.post(
    "/api/v1/applications",
    summary="Submit a financial assistance application",
    responses={
        200: {"description": "Application submitted"},
        422: {"description": "Validation error"},
        429: {"description": "Too many submissions"},
    },
)(response_wrapper(submit_application_view))

# Admin
router.get(
    "/api/v1/admin/applications",
    summary="Admin: list applications with search and status filters",
    responses={200: {"description": "Paginated admin view"}, 403: {"description": "Not an admin"}},
)(response_wrapper(list_applications_admin))

router.get(
    "/api/v1/admin/applications/{application_id}",
    summary="Admin: get application by ID",
    responses={
        200: {"description": "Application detail"},
        403: {"description": "Not an admin"},
        404: {"description": "Not found"},
    },
)(response_wrapper(get_application_view))

router.patch(
    "/api/v1/admin/applications/{application_id}/status",
    summary="Admin: update application status",
    responses={
        200: {"description": "Status updated"},
        403: {"description": "Not an admin"},
        404: {"description": "Not found"},
    },
)(response_wrapper(update_application_status_view))
