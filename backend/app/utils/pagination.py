# backend/app/utils/pagination.py
"""Pagination utilities"""

from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool


def paginate(items: list, page: int = 1, page_size: int = 20) -> dict:
    """Simple pagination helper."""
    start = (page - 1) * page_size
    end = start + page_size
    total = len(items)
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }
