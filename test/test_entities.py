import sys
import os
import pytest
from pydantic import ValidationError

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.entities.products_entities import Product, UpdateProduct


class TestProductEntity:
    """Test cases for Product entity"""

    def test_product_valid_data(self):
        """Test Product entity with valid data"""
        product_data = {
            "product": {
                "id": "test-product-id-123",
                "name": "Test Product",
                "price": 150.0
            }
        }
        
        product = Product(**product_data)
        assert product.product["id"] == "test-product-id-123"
        assert product.product["name"] == "Test Product"
        assert product.product["price"] == 150.0

    def test_product_missing_product_field(self):
        """Test Product entity with missing product field"""
        with pytest.raises(ValidationError):
            Product(id="test-product-id-123")

    def test_product_empty_product_field(self):
        """Test Product entity with empty product field - should be valid"""
        product_data = {
            "product": {}
        }
        
        # This should work as Dict[str, Any] allows empty dictionaries
        product = Product(**product_data)
        assert product.product == {}

    def test_product_invalid_product_type(self):
        """Test Product entity with invalid product type"""
        with pytest.raises(ValidationError):
            Product(product="invalid_string")


class TestUpdateProductEntity:
    """Test cases for UpdateProduct entity"""

    def test_update_product_valid_data(self):
        """Test UpdateProduct entity with valid data"""
        update_data = {
            "id": "test-product-id-123",
            "name": "Updated Test Product",
            "price": 200.0
        }
        
        update_product = UpdateProduct(**update_data)
        assert update_product.id == "test-product-id-123"
        assert update_product.name == "Updated Test Product"
        assert update_product.price == 200.0

    def test_update_product_missing_id(self):
        """Test UpdateProduct entity with missing id"""
        with pytest.raises(ValidationError):
            UpdateProduct(name="Test Product", price=150.0)

    def test_update_product_missing_name(self):
        """Test UpdateProduct entity with missing name"""
        with pytest.raises(ValidationError):
            UpdateProduct(id="test-product-id-123", price=150.0)

    def test_update_product_missing_price(self):
        """Test UpdateProduct entity with missing price"""
        with pytest.raises(ValidationError):
            UpdateProduct(id="test-product-id-123", name="Test Product")

    def test_update_product_invalid_price_type(self):
        """Test UpdateProduct entity with invalid price type"""
        with pytest.raises(ValidationError):
            UpdateProduct(id="test-product-id-123", name="Test Product", price="invalid_price")

    def test_update_product_negative_price(self):
        """Test UpdateProduct entity with negative price"""
        update_data = {
            "id": "test-product-id-123",
            "name": "Test Product",
            "price": -50.0
        }
        
        # This should work as there's no validation for negative prices
        update_product = UpdateProduct(**update_data)
        assert update_product.price == -50.0 