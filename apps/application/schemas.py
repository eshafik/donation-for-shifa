from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ApplicationCreate(BaseModel):
    applicant_name: str
    applicant_phone: Optional[str] = None
    applicant_address: str = Field(min_length=5)
    problem_description: str = Field(min_length=20)
    amount_requested: Optional[Decimal] = Field(default=None, gt=0)


class ApplicationSubmitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submitted_at: datetime


class ApplicationAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    applicant_name: str
    applicant_phone: Optional[str]
    applicant_address: str
    problem_description: str
    amount_requested: Optional[Decimal]
    status: str
    admin_notes: Optional[str]
    submitted_at: datetime
    updated_at: datetime
    reviewed_by_id: Optional[int]


class ApplicationStatusUpdate(BaseModel):
    status: Literal["reviewed", "approved", "rejected"]
    admin_notes: Optional[str] = None
