from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DonationCreate(BaseModel):
    donor_name:         str     = Field(..., min_length=1, max_length=255)
    transaction_number: str     = Field(..., min_length=1, max_length=100)
    amount:             Decimal = Field(..., gt=0)
    date_received:      date
    notes:              Optional[str] = None


class DonationUpdate(BaseModel):
    donor_name:         Optional[str]     = Field(None, min_length=1, max_length=255)
    transaction_number: Optional[str]     = Field(None, min_length=1, max_length=100)
    amount:             Optional[Decimal] = Field(None, gt=0)
    date_received:      Optional[date]    = None
    notes:              Optional[str]     = None


class DonationPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:                 int
    donor_name:         str
    transaction_number: str
    amount:             Decimal
    date_received:      date


class DonationAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:                 int
    donor_name:         str
    transaction_number: str
    amount:             Decimal
    date_received:      date
    notes:              Optional[str] = None
    created_at:         datetime
    updated_at:         datetime
    created_by_id:      Optional[int] = None
