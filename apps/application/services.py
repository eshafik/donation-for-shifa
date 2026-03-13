from typing import Any, Dict, Optional

from tortoise.expressions import Q

from apps.application.models import DonationApplication
from apps.user.models import User
from utils.pagination import paginate


async def create_application(data: dict) -> DonationApplication:
    app = await DonationApplication.create(**data)
    return await DonationApplication.get(id=app.id)


async def get_applications_admin(
    page: int,
    size: int,
    search: Optional[str],
    status: Optional[str],
) -> Dict[str, Any]:
    qs = DonationApplication.all()
    if search:
        qs = qs.filter(
            Q(applicant_name__icontains=search) | Q(applicant_address__icontains=search)
        )
    if status:
        qs = qs.filter(status=status)
    return await paginate(qs, page, size)


async def get_application_by_id(application_id: int) -> DonationApplication:
    return await DonationApplication.get(id=application_id)


async def update_application_status(
    application_id: int, status: str, admin_notes: Optional[str], reviewer: User
) -> DonationApplication:
    application = await DonationApplication.get(id=application_id)
    application.status = status
    if admin_notes is not None:
        application.admin_notes = admin_notes
    application.reviewed_by = reviewer
    await application.save()
    return await DonationApplication.get(id=application_id)
