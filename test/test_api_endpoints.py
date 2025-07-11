import sys
import os
import pytest
import json
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.main import app

client = TestClient(app)

class TestInventoryAPIEndpoints:
    """Test class for inventory API endpoints"""

    def test_get_products_endpoint_success(self):
        """Test successful get products endpoint"""
        # Mock the HTTP call made by the controller
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "products": [
                {
                    "id": "test-product-id-123",
                    "name": "Test Product",
                    "price": 150.0
                }
            ]
        }).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test data
            product_data = {
                "product": {
                    "id": "test-product-id-123"
                }
            }

            # Make request
            response = client.post("/api-inventory/products/", json=product_data)

            # Assertions
            assert response.status_code == 200
            assert "result" in response.json()
            assert "products" in response.json()["result"]

    def test_get_products_endpoint_invalid_data(self):
        """Test get products endpoint with invalid data - should pass since Product allows any dict"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test with invalid product data - Product entity allows any dict
            invalid_data = {
                "product": {
                    "invalid_field": "invalid_value"
                }
            }

            response = client.post("/api-inventory/products/", json=invalid_data)

            # Should return 200 since Product allows any dictionary
            assert response.status_code == 200

    def test_get_products_endpoint_missing_data(self):
        """Test get products endpoint with missing data"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test with missing product data
            invalid_data = {
                "wrong_field": "value"
            }

            response = client.post("/api-inventory/products/", json=invalid_data)

            # Should return 422 for validation error - missing required 'product' field
            assert response.status_code == 422

    def test_get_products_endpoint_controller_error(self):
        """Test get products endpoint when controller raises an error"""
        # Mock HTTP error
        with patch('urllib.request.urlopen', side_effect=Exception("Connection failed")):
            product_data = {
                "product": {
                    "id": "test-product-id-123"
                }
            }

            response = client.post("/api-inventory/products/", json=product_data)

            # Should return 500 for internal server error
            assert response.status_code == 500

    def test_update_product_endpoint_success(self):
        """Test successful update product endpoint"""
        # Mock the HTTP call made by the controller
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "result": "success",
            "product": {
                "id": "test-product-id-123",
                "name": "Updated Test Product",
                "price": 200.0
            }
        }).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test data - only product ID as per your validation
            update_data = {
                "product": {
                    "id": "test-product-id-123"
                }
            }

            # Make request
            response = client.post("/api-inventory/update-product/", json=update_data)

            # Assertions
            assert response.status_code == 200
            assert "result" in response.json()

    def test_update_product_endpoint_invalid_data(self):
        """Test update product endpoint with invalid data - should pass since Product allows any dict"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test with invalid update data - Product entity allows any dictionary
            invalid_data = {
                "product": {
                    # Missing id field but Product allows any dict
                }
            }

            response = client.post("/api-inventory/update-product/", json=invalid_data)

            # Should return 200 since Product allows any dictionary
            assert response.status_code == 200

    def test_update_product_endpoint_missing_product_field(self):
        """Test update product endpoint with missing product field"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test with missing product field
            invalid_data = {
                "wrong_field": {
                    "id": "test-product-id-123"
                }
            }

            response = client.post("/api-inventory/update-product/", json=invalid_data)

            # Should return 422 for validation error - missing required 'product' field
            assert response.status_code == 422

    def test_update_product_endpoint_empty_product_field(self):
        """Test update product endpoint with empty product field - should pass since Product allows any dict"""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test with empty product field - Product entity allows empty dictionaries
            invalid_data = {
                "product": {}
            }

            response = client.post("/api-inventory/update-product/", json=invalid_data)

            # Should return 200 since Product allows empty dictionaries
            assert response.status_code == 200

    def test_update_product_endpoint_controller_error(self):
        """Test update product endpoint when controller raises an error"""
        # Mock HTTP error
        with patch('urllib.request.urlopen', side_effect=Exception("Update failed")):
            update_data = {
                "product": {
                    "id": "test-product-id-123"
                }
            }

            response = client.post("/api-inventory/update-product/", json=update_data)

            # Should return 500 for internal server error
            assert response.status_code == 500

    def test_endpoints_content_type(self):
        """Test that endpoints return correct content type"""
        # Mock successful responses for content type tests
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test get products endpoint
            product_data = {
                "product": {
                    "id": "test-product-id-123"
                }
            }

            response = client.post("/api-inventory/products/", json=product_data)
            assert response.headers["content-type"] == "application/json"

            # Test update product endpoint
            update_data = {
                "product": {
                    "id": "test-product-id-123"
                }
            }

            response = client.post("/api-inventory/update-product/", json=update_data)
            assert response.headers["content-type"] == "application/json"

    def test_update_product_with_real_id(self):
        """Test update product endpoint with real database ID"""
        # Mock the HTTP call made by the controller
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "result": "success",
            "product": {
                "_id": "68708c59422d94d1e5b72eaf",
                "name": "pages",
                "price": 9000333
            }
        }).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            # Test data with real database ID
            update_data = {
                "product": {
                    "id": "68708c59422d94d1e5b72eaf"
                }
            }

            # Make request
            response = client.post("/api-inventory/update-product/", json=update_data)

            # Assertions
            assert response.status_code == 200
            assert "result" in response.json()
            assert "product" in response.json()["result"]
            assert response.json()["result"]["product"]["_id"] == "68708c59422d94d1e5b72eaf"
            assert response.json()["result"]["product"]["name"] == "pages"
            assert response.json()["result"]["product"]["price"] == 9000333 