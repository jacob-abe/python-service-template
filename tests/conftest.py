"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from supabase import Client
from app.main import create_application
from app.core.config import settings


@pytest.fixture(scope="session")
def app():
    """Create FastAPI application for testing."""
    return create_application()


@pytest.fixture(scope="function")
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def mock_db():
    """
    Mock Supabase database client.
    
    Usage:
        def test_something(mock_db):
            mock_db.table.return_value.select.return_value.execute.return_value.data = [...]
    """
    mock_client = Mock(spec=Client)
    return mock_client


@pytest.fixture(scope="function")
def override_get_db(mock_db):
    """
    Override database dependency with mock.
    
    Usage:
        def test_endpoint(client, override_get_db):
            app.dependency_overrides[get_db] = lambda: mock_db
            response = client.get("/api/items")
    """
    from app.core.database import get_db
    from app.main import app
    
    app.dependency_overrides[get_db] = lambda: mock_db
    yield mock_db
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers():
    """Fixture for authentication headers."""
    return {
        "Authorization": "Bearer test-token",
        "X-API-Key": "test-api-key"
    }


@pytest.fixture(scope="function")
def sample_item():
    """Fixture for sample item data."""
    return {
        "id": "123",
        "name": "Test Item",
        "description": "A test item"
    }

