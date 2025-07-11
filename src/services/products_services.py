from fastapi import Header, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

import asyncio
import json
import traceback
import urllib.request


from src.utils.logger_utils import Log
from src.entities.products_entities import Product, UpdateProduct
from src.controllers.get_products_controllers import GetProducts
from src.controllers.update_products_controllers import UpdateProducts
from src.utils.error_handling import ErrorHandler


log = Log()
router = APIRouter(prefix="/api-inventory")


############################################################################################################
# endpoints to get information Products
############################################################################################################

# request of ammount of products for id

@router.post('/products/')
async def get_products(product_id: Product):
    """
    This function is used to get all products
    :return: all products
    """
    try:
        log.logger.info("Fetching all products")
        request = product_id
        response_data = await GetProducts(request).get_products()
        # Return the data directly without double serialization
        return JSONResponse(content={"result": response_data}, status_code=200)
    except Exception as error:
        return ErrorHandler.handle_error(error, "Error fetching products")


# endpoint to update a product by id
@router.post('/update-product/')
async def update_product(product_id: Product):
    """
    This function is used to update a product by id
    :param product: Product object containing the updated information
    :return: Updated product information
    """
    try:
        request = product_id.model_dump()
        response = await UpdateProducts(request).update_product()
        return JSONResponse(content={"result": response}, status_code=200)
    except Exception as error:
        return ErrorHandler.handle_error(error, "Error updating product")
    

# endpoint healt check
@router.get('/health/')
async def health_check():
    """
    This function is used to check the health of the inventory service
    :return: health status
    """
    return JSONResponse(content={"status": "success", "message": "Inventory service is running"}, status_code=200)



