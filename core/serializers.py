"""
Base Pydantic and Tortoise serialization patterns (DRF-like).

- Input schemas: plain BaseModel for create/update (no from_attributes).
- Response schemas: use model_config = ConfigDict(from_attributes=True) for ORM-backed models,
  or tortoise.contrib.pydantic.pydantic_model_creator for generated schemas with relations.
- Pattern: services return Tortoise instances; views convert via Schema.model_validate(orm_instance)
  or await Schema.from_tortoise_orm(instance) for Tortoise-generated schemas.
"""
from pydantic import BaseModel, ConfigDict


def orm_response_config() -> ConfigDict:
    """Config for Pydantic response models built from Tortoise ORM (from_attributes=True)."""
    return ConfigDict(from_attributes=True)
