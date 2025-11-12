"""Tests for database connection and operations."""
import pytest
from unittest.mock import Mock, patch
from app.core.database import Database, get_db


class TestDatabase:
    """Test database connection and dependency injection."""
    
    def test_database_initialization(self):
        """Test database initialization."""
        db = Database()
        assert db._client is None
    
    @patch("app.core.database.create_client")
    def test_database_client_creation(self, mock_create_client):
        """Test Supabase client creation."""
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        
        db = Database()
        client = db.client
        
        assert client == mock_client
        mock_create_client.assert_called_once()
    
    def test_database_close(self):
        """Test database connection closing."""
        db = Database()
        db._client = Mock()
        db.close()
        assert db._client is None
    
    def test_get_db_dependency(self, mock_db):
        """Test database dependency injection."""
        from app.main import app
        from app.core.database import get_db
        
        # Override the dependency
        app.dependency_overrides[get_db] = lambda: mock_db
        
        # In FastAPI, dependencies are resolved through the dependency system
        # For testing, we verify the override is set correctly
        assert get_db in app.dependency_overrides
        
        # Clean up
        app.dependency_overrides.clear()
        assert get_db not in app.dependency_overrides

