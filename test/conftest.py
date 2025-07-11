import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.main import app

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture
def mock_product_data():
    """Sample product data for testing"""
    return {
        "product": {
            "id": "test-product-id-123",
            "name": "Test Product",
            "price": 150.0
        }
    }

@pytest.fixture
def mock_update_product_data():
    """Sample update product data for testing"""
    return {
        "product": {
            "id": "test-product-id-123",
            "name": "Updated Test Product",
            "price": 200.0
        }
    }

@pytest.fixture
def mock_product_response():
    """Mock response from product service"""
    return {
        "result": {
            "data": {
                "product": {
                    "id": "test-product-id-123",
                    "name": "Test Product",
                    "price": 150.0
                }
            }
        }
    }

@pytest.fixture
def mock_update_response():
    """Mock response from update service"""
    return {
        "result": {
            "data": {
                "product": {
                    "id": "test-product-id-123",
                    "name": "Updated Test Product",
                    "price": 200.0
                }
            }
        }
    } 