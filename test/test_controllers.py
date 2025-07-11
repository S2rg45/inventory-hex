import sys
import os
import pytest
import json
import asyncio
from unittest.mock import patch, Mock, MagicMock
from urllib.error import HTTPError, URLError
from fastapi import HTTPException

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.controllers.get_products_controllers import GetProducts
from src.controllers.update_products_controllers import UpdateProducts
from src.entities.products_entities import Product


class TestGetProductsController:
    """Test cases for GetProducts controller"""

    @pytest.mark.asyncio
    async def test_get_products_success(self):
        """Test successful product retrieval"""
        product_id = Product(product={"id": "test-product-id-123"})
        
        # Create a proper mock response object
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"products": []}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            controller = GetProducts(product_id)
            result = await controller.get_products()
            
            assert result == {"products": []}

    @pytest.mark.asyncio
    async def test_get_products_invalid_json_response(self):
        """Test get products with invalid JSON response"""
        product_id = Product(product={"id": "test-product-id-123"})
        
        # Mock invalid JSON response
        mock_response = Mock()
        mock_response.read.return_value = "invalid json".encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            controller = GetProducts(product_id)
            
            with pytest.raises(HTTPException) as exc_info:
                await controller.get_products()
            
            assert exc_info.value.status_code == 500
            assert "Expecting value" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_products_request_encoding(self):
        """Test that get request data is properly encoded"""
        product_id = Product(product={"id": "test-product-id-123"})
        
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"products": []}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response) as mock_urlopen:
            controller = GetProducts(product_id)
            await controller.get_products()
            
            # Verify the request was made with proper encoding
            mock_urlopen.assert_called_once()
            call_args = mock_urlopen.call_args[0][0]
            assert call_args.data == json.dumps(product_id.model_dump()).encode("utf-8")


class TestUpdateProductsController:
    """Test cases for UpdateProducts controller"""

    @pytest.mark.asyncio
    async def test_update_product_success(self):
        """Test successful product update"""
        product_data = {
            "product": {
                "id": "test-product-id-123"
            }
        }
        
        # Create a proper mock response object
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            controller = UpdateProducts(product_data)
            result = await controller.update_product()
            
            assert result == {"result": "success"}

    @pytest.mark.asyncio
    async def test_update_product_invalid_json_response(self):
        """Test update product with invalid JSON response"""
        product_data = {
            "product": {
                "id": "test-product-id-123"
            }
        }
        
        # Mock invalid JSON response
        mock_response = Mock()
        mock_response.read.return_value = "invalid json".encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response):
            controller = UpdateProducts(product_data)
            
            with pytest.raises(HTTPException) as exc_info:
                await controller.update_product()
            
            assert exc_info.value.status_code == 500
            assert "Expecting value" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_update_product_request_encoding(self):
        """Test that update request data is properly encoded"""
        product_data = {
            "product": {
                "id": "test-product-id-123"
            }
        }
        
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"result": "success"}).encode('utf-8')
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        
        with patch('urllib.request.urlopen', return_value=mock_response) as mock_urlopen:
            controller = UpdateProducts(product_data)
            await controller.update_product()
            
            # Verify the request was made with proper encoding
            mock_urlopen.assert_called_once()
            call_args = mock_urlopen.call_args[0][0]
            assert call_args.data == json.dumps(product_data).encode("utf-8") 