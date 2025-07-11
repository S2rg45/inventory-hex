
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class Product(BaseModel):
    product: Dict[str, Any] = Field(..., description="Product data containing id, name, and price", example=[{"id": "12345","name": "Sample Product","price": 1990}])


class UpdateProduct(BaseModel):
    id: str = Field(..., description="Unique identifier for the product", example="12345")
    name: str = Field(..., description="Name of the product", example="Sample Product")
    price: float = Field(..., description="Price of the product in cents", example=1990.0)