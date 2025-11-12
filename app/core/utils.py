"""Core utility functions and decorators."""
from functools import wraps
from typing import Callable, Any
from inspect import iscoroutinefunction
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


def handle_exceptions(
    operation_name: str = "operation",
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
):
    """
    Decorator to handle exceptions in API endpoints.
    
    Args:
        operation_name: Name of the operation for error messages
        status_code: HTTP status code to return on error (default: 500)
    
    Usage:
        @router.get("/items")
        @handle_exceptions(operation_name="fetching items")
        async def get_items():
            # Your code here
            pass
    """
    def decorator(func: Callable) -> Callable:
        if iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return await func(*args, **kwargs)
                except HTTPException:
                    # Re-raise HTTPExceptions as-is
                    raise
                except Exception as e:
                    logger.error(
                        f"Error {operation_name}: {str(e)}",
                        exc_info=True
                    )
                    raise HTTPException(
                        status_code=status_code,
                        detail=f"Error {operation_name}: {str(e)}"
                    )
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except HTTPException:
                    # Re-raise HTTPExceptions as-is
                    raise
                except Exception as e:
                    logger.error(
                        f"Error {operation_name}: {str(e)}",
                        exc_info=True
                    )
                    raise HTTPException(
                        status_code=status_code,
                        detail=f"Error {operation_name}: {str(e)}"
                    )
            return sync_wrapper
    
    return decorator

