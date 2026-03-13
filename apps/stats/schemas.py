
# stats/schemas.py
from pydantic import BaseModel, ConfigDict


class ExampleCreate(BaseModel):
    name: str


class ExampleUpdate(BaseModel):
    name: str | None = None


class ExampleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
