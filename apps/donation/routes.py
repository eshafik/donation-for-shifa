from fastapi import APIRouter

from utils.response_wrapper import response_wrapper
from .views import (
    create_donation_view,
    delete_donation_view,
    get_donation_view,
    list_donations_admin,
    list_donations_public,
    update_donation_view,
)

router = APIRouter(tags=["donation"])

# Public
router.get(
    "/api/v1/donations",
    summary="List received donations",
    responses={200: {"description": "Paginated list of donations"}},
)(response_wrapper(list_donations_public))

# Admin
router.get(
    "/api/v1/admin/donations",
    summary="Admin: list donations with search and date filters",
    responses={200: {"description": "Paginated admin view"}, 403: {"description": "Not an admin"}},
)(response_wrapper(list_donations_admin))

router.post(
    "/api/v1/admin/donations",
    summary="Admin: create a donation record",
    responses={200: {"description": "Created donation"}, 403: {"description": "Not an admin"}, 409: {"description": "Duplicate transaction number"}},
)(response_wrapper(create_donation_view))

router.get(
    "/api/v1/admin/donations/{donation_id}",
    summary="Admin: get donation by ID",
    responses={200: {"description": "Donation detail"}, 403: {"description": "Not an admin"}, 404: {"description": "Not found"}},
)(response_wrapper(get_donation_view))

router.put(
    "/api/v1/admin/donations/{donation_id}",
    summary="Admin: update a donation record",
    responses={200: {"description": "Updated donation"}, 403: {"description": "Not an admin"}, 404: {"description": "Not found"}},
)(response_wrapper(update_donation_view))

router.delete(
    "/api/v1/admin/donations/{donation_id}",
    summary="Admin: delete a donation record",
    responses={200: {"description": "Deleted"}, 403: {"description": "Not an admin"}, 404: {"description": "Not found"}},
)(response_wrapper(delete_donation_view))
