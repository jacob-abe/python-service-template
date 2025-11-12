"""Generic authentication middleware skeleton."""
from typing import Optional
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    
    # Common auth header names that might be used
    AUTH_HEADER_NAMES = [
        "authorization",
        "x-api-key",
        "x-auth-token",
        "x-access-token",
        "bearer",
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Extract auth headers
        auth_headers = self._extract_auth_headers(request)
        
        # Log intercepted headers (for debugging)
        if auth_headers:
            logger.info(f"Intercepted auth headers: {auth_headers}")
            # Print to console as requested
            print(f"[Auth Middleware] Intercepted auth headers: {auth_headers}")
        else:
            logger.debug("No auth headers found in request")
            print("[Auth Middleware] No auth headers found in request")
        
        # Validate authentication (skeleton - implement actual validation)
        auth_result = await self._validate_auth(request, auth_headers)
        
        if not auth_result.is_valid:
            logger.warning(
                f"Authentication validation failed for {request.url.path}: "
                f"{auth_result.reason}"
            )
            print(f"[Auth Middleware] Validation failed: {auth_result.reason}")
        
        # Add auth info to request state for use in route handlers
        request.state.auth = auth_result
        
        # Continue with request
        response = await call_next(request)
        return response
    
    def _extract_auth_headers(self, request: Request) -> dict:
        """Extract authentication-related headers from request."""
        auth_headers = {}
        
        for header_name in self.AUTH_HEADER_NAMES:
            header_value = request.headers.get(header_name) or request.headers.get(
                header_name.replace("-", "_")
            )
            if header_value:
                auth_headers[header_name] = header_value
        
        return auth_headers
    
    async def _validate_auth(
        self, request: Request, auth_headers: dict
    ) -> "AuthResult":

        # TODO: Implement actual authentication validation
        # Example for Auth0:
        # - Extract token from Authorization header
        # - Validate JWT signature
        # - Check token expiration
        # - Verify audience and issuer
        
        if not auth_headers:
            return AuthResult(
                is_valid=False,
                reason="No authentication headers provided",
                user_id=None,
                token=None
            )
        
        # Placeholder: Always return valid for skeleton
        # In production, implement actual validation
        return AuthResult(
            is_valid=True,
            reason="Skeleton implementation - validation not yet implemented",
            user_id=None,
            token=auth_headers.get("authorization") or auth_headers.get("x-api-key")
        )


class AuthResult:

    def __init__(
        self,
        is_valid: bool,
        reason: str,
        user_id: Optional[str] = None,
        token: Optional[str] = None,
    ):
        self.is_valid = is_valid
        self.reason = reason
        self.user_id = user_id
        self.token = token

