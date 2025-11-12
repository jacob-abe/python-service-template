"""Tests for logging middleware."""
import pytest
import logging
from unittest.mock import Mock, AsyncMock, patch
from fastapi import Request, Response
from app.middleware.logging_middleware import LoggingMiddleware, logger


class TestLoggingMiddleware:
    """Test logging middleware."""
    
    @pytest.fixture
    def logging_middleware(self):
        """Create logging middleware instance."""
        app = Mock()
        return LoggingMiddleware(app)
    
    @pytest.fixture
    def mock_request(self):
        """Create mock request."""
        request = Mock(spec=Request)
        request.method = "GET"
        request.url.path = "/test"
        request.client.host = "127.0.0.1"
        request.headers = {}
        request.query_params = {}
        return request
    
    @pytest.fixture
    def mock_response(self):
        """Create mock response."""
        from starlette.datastructures import MutableHeaders
        
        response = Mock(spec=Response)
        response.status_code = 200
        # Use MutableHeaders which is what FastAPI/Starlette actually uses
        response.headers = MutableHeaders()
        return response
    
    @pytest.mark.asyncio
    async def test_logging_middleware_success(
        self, logging_middleware, mock_request, mock_response
    ):
        """Test logging middleware with successful request."""
        # Use a real async function instead of AsyncMock to avoid coroutine issues
        async def call_next(request):
            return mock_response
        
        # Don't patch time.time - just verify the middleware works
        # The time calculation will use real time, which is fine for this test
        response = await logging_middleware.dispatch(mock_request, call_next)
        
        assert response == mock_response
        assert "X-Process-Time" in response.headers
        # Verify the header contains a valid time string (should be a float as string)
        process_time = float(response.headers["X-Process-Time"])
        assert process_time >= 0
    
    @pytest.mark.asyncio
    async def test_logging_middleware_error(
        self, logging_middleware, mock_request
    ):
        """Test logging middleware with error."""
        call_next = AsyncMock(side_effect=Exception("Test error"))
        
        with patch("app.middleware.logging_middleware.time.time", side_effect=[0.0, 0.1]):
            with pytest.raises(Exception):
                await logging_middleware.dispatch(mock_request, call_next)
    
    def test_logger_configuration(self):
        """Test that logger is properly configured."""
        assert logger is not None
        assert isinstance(logger, logging.Logger)

