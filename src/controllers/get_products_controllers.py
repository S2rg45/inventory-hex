

from fastapi import Header, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import JSONResponse

import urllib.request
import json
import traceback
import httpx

from src.utils.logger_utils import Log
from src.utils.error_handling import ErrorHandler


class GetProducts:
    """
    This class is used to get all products
    """
    def __init__(self, product_id):
        self.log = Log()
        self.product_id = product_id

    async def get_products(self):
        try:
            self.log.logger.info("Fetching all products")
            url="http://ms-product:8000/api-products/product/"
            params = self.product_id.model_dump()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    json=params,
                    headers={"Content-Type": "application/json"}
                )
            resp_data = response.json()
            self.log.logger.info(f"Products fetched successfully: {resp_data}")
            # Return only the data, not a JSONResponse
            return resp_data
        except Exception as error:
            raise ErrorHandler.handle_error(error, "Error fetching products")
        

    