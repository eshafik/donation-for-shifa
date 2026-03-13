from enum import Enum

from tortoise import fields, models


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


class DonationApplication(models.Model):
    id = fields.BigIntField(pk=True)
    applicant_name = fields.CharField(max_length=255)
    applicant_phone = fields.CharField(max_length=30, null=True)
    applicant_address = fields.TextField()
    problem_description = fields.TextField()
    amount_requested = fields.DecimalField(max_digits=12, decimal_places=2, null=True)
    status = fields.CharEnumField(ApplicationStatus, default=ApplicationStatus.PENDING, max_length=20)
    admin_notes = fields.TextField(null=True)
    submitted_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    reviewed_by = fields.ForeignKeyField("user.User", null=True, on_delete=fields.SET_NULL)

    class Meta:
        table = "donation_applications"
        ordering = ["-submitted_at"]
