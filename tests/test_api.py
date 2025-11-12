"""Tests for API endpoints."""
import pytest
from unittest.mock import Mock
from app.api.endpoints.items import get_items, create_item


class TestItemsEndpoint:
    """Test items API endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_items(self, mock_db):
        """Test getting items."""
        # Mock database response
        mock_db.table.return_value.select.return_value.range.return_value.execute.return_value.data = [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "name": "Item 2"}
        ]
        
        result = await get_items(skip=0, limit=10, db=mock_db)
        assert isinstance(result, list)
        assert len(result) > 0
        assert "message" in result[0]
    
    @pytest.mark.asyncio
    async def test_create_item(self, mock_db, sample_item):
        """Test creating an item."""
        # Mock database response
        mock_db.table.return_value.insert.return_value.execute.return_value.data = [sample_item]
        
        result = await create_item(item=sample_item, db=mock_db)
        assert isinstance(result, dict)
        assert "message" in result


class TestAPIEndpoints:
    """Test API endpoints with test client."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_items_endpoint(self, client, override_get_db):
        """Test items endpoint."""
        response = client.get("/api/items")
        assert response.status_code == 200
    
    def test_swagger_docs(self, client):
        """Test Swagger documentation endpoint."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema(self, client):
        """Test OpenAPI schema endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data

