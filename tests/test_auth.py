"""Tests for authentication middleware."""
import pytest
from fastapi import Request
from unittest.mock import Mock, AsyncMock
from app.middleware.auth_middleware import AuthMiddleware, AuthResult


class TestAuthMiddleware:
    """Test authentication middleware."""
    
    @pytest.fixture
    def auth_middleware(self):
        """Create auth middleware instance."""
        app = Mock()
        return AuthMiddleware(app)
    
    @pytest.fixture
    def mock_request(self):
        """Create mock request."""
        request = Mock(spec=Request)
        request.headers = {}
        request.url.path = "/test"
        return request
    
    def test_extract_auth_headers_no_headers(self, auth_middleware, mock_request):
        """Test extracting auth headers when none are present."""
        auth_headers = auth_middleware._extract_auth_headers(mock_request)
        assert auth_headers == {}
    
    def test_extract_auth_headers_with_authorization(self, auth_middleware, mock_request):
        """Test extracting authorization header."""
        mock_request.headers = {"authorization": "Bearer test-token"}
        auth_headers = auth_middleware._extract_auth_headers(mock_request)
        assert "authorization" in auth_headers
        assert auth_headers["authorization"] == "Bearer test-token"
    
    def test_extract_auth_headers_with_api_key(self, auth_middleware, mock_request):
        """Test extracting API key header."""
        mock_request.headers = {"x-api-key": "test-api-key"}
        auth_headers = auth_middleware._extract_auth_headers(mock_request)
        assert "x-api-key" in auth_headers
        assert auth_headers["x-api-key"] == "test-api-key"
    
    @pytest.mark.asyncio
    async def test_validate_auth_no_headers(self, auth_middleware, mock_request):
        """Test auth validation with no headers."""
        result = await auth_middleware._validate_auth(mock_request, {})
        assert result.is_valid is False
        assert "No authentication headers" in result.reason
    
    @pytest.mark.asyncio
    async def test_validate_auth_with_headers(self, auth_middleware, mock_request):
        """Test auth validation with headers (skeleton implementation)."""
        auth_headers = {"authorization": "Bearer test-token"}
        result = await auth_middleware._validate_auth(mock_request, auth_headers)
        # Skeleton implementation returns valid
        assert result.is_valid is True
        assert result.token is not None


class TestAuthResult:
    """Test AuthResult class."""
    
    def test_auth_result_creation(self):
        """Test creating AuthResult."""
        result = AuthResult(
            is_valid=True,
            reason="Test reason",
            user_id="user123",
            token="token123"
        )
        assert result.is_valid is True
        assert result.reason == "Test reason"
        assert result.user_id == "user123"
        assert result.token == "token123"

