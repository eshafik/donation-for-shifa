"""Common FastAPI dependencies (pagination, etc.)."""
from typing import Annotated

from fastapi import Query


def pagination_params(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="Page size")] = 10,
) -> tuple[int, int]:
    """Dependency for pagination; returns (page, size)."""
    return page, size
