from fastapi import APIRouter

from utils.response_wrapper import response_wrapper
from .views import (
    create_distribution_view,
    delete_distribution_view,
    get_distribution_view,
    list_distributions_admin,
    list_distributions_public,
    update_distribution_view,
)

router = APIRouter(tags=["distribution"])

# Public
router.get(
    "/api/v1/distributions",
    summary="List distributions to recipients",
    responses={200: {"description": "Paginated list of distributions"}},
)(response_wrapper(list_distributions_public))

# Admin
router.get(
    "/api/v1/admin/distributions",
    summary="Admin: list distributions with search and date filters",
    responses={200: {"description": "Paginated admin view"}, 403: {"description": "Not an admin"}},
)(response_wrapper(list_distributions_admin))

router.post(
    "/api/v1/admin/distributions",
    summary="Admin: create a distribution record",
    responses={200: {"description": "Created distribution"}, 403: {"description": "Not an admin"}},
)(response_wrapper(create_distribution_view))

router.get(
    "/api/v1/admin/distributions/{distribution_id}",
    summary="Admin: get distribution by ID",
    responses={200: {"description": "Distribution detail"}, 403: {"description": "Not an admin"}, 404: {"description": "Not found"}},
)(response_wrapper(get_distribution_view))

router.put(
    "/api/v1/admin/distributions/{distribution_id}",
    summary="Admin: update a distribution record",
    responses={200: {"description": "Updated distribution"}, 403: {"description": "Not an admin"}, 404: {"description": "Not found"}},
)(response_wrapper(update_distribution_view))

router.delete(
    "/api/v1/admin/distributions/{distribution_id}",
    summary="Admin: delete a distribution record",
    responses={200: {"description": "Deleted"}, 403: {"description": "Not an admin"}, 404: {"description": "Not found"}},
)(response_wrapper(delete_distribution_view))
