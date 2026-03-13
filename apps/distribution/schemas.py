from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DistributionCreate(BaseModel):
    recipient_name:      str     = Field(..., min_length=1, max_length=255)
    address:             str     = Field(..., min_length=5)
    problem_description: str     = Field(..., min_length=10)
    amount_received:     Decimal = Field(..., gt=0)
    date_distributed:    date
    notes:               Optional[str] = None


class DistributionUpdate(BaseModel):
    recipient_name:      Optional[str]     = Field(None, min_length=1, max_length=255)
    address:             Optional[str]     = Field(None, min_length=5)
    problem_description: Optional[str]     = Field(None, min_length=10)
    amount_received:     Optional[Decimal] = Field(None, gt=0)
    date_distributed:    Optional[date]    = None
    notes:               Optional[str]     = None


class DistributionPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:                  int
    recipient_name:      str
    address:             str
    problem_description: str
    amount_received:     Decimal
    date_distributed:    date


class DistributionAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:                  int
    recipient_name:      str
    address:             str
    problem_description: str
    amount_received:     Decimal
    date_distributed:    date
    notes:               Optional[str] = None
    created_at:          datetime
    updated_at:          datetime
    created_by_id:       Optional[int] = None
