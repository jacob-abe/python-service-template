"""Example items endpoint."""
from fastapi import APIRouter, Depends
from typing import List
from supabase import Client
from app.core.database import DatabaseDep
from app.core.utils import handle_exceptions

router = APIRouter()


@router.get("/")
@handle_exceptions(operation_name="fetching items")
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: DatabaseDep = None
) -> List[dict]:
    return [
        {
            "message": "Items endpoint - implement actual database queries",
            "skip": skip,
            "limit": limit
        }
    ]


@router.post("/")
@handle_exceptions(operation_name="creating item")
async def create_item(
    item: dict,
    db: DatabaseDep = None
) -> dict:
    return {
        "message": "Create item endpoint - implement actual database insert",
        "item": item
    }

