"""Database connection and dependency injection for Supabase."""
from typing import Annotated, Optional
from fastapi import Depends
from supabase import create_client, Client
from app.core.config import settings


class Database:
    """Database connection manager for Supabase."""
    
    def __init__(self):
        self._client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Get or create Supabase client."""
        if self._client is None:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return self._client
    
    def close(self):
        """Close database connection (if needed)."""
        # Supabase client doesn't require explicit closing, but we can reset it
        self._client = None


# Global database instance
_db = Database()


def get_db() -> Client:
    """
    Dependency injection for Supabase client.
    
    Usage:
        @app.get("/items")
        def get_items(db: Annotated[Client, Depends(get_db)]):
            ...
    """
    return _db.client


# Type alias for dependency injection
DatabaseDep = Annotated[Client, Depends(get_db)]

