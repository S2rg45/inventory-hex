
from fastapi import Header, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import JSONResponse

import urllib.request
import json
import traceback
import httpx

from src.utils.logger_utils import Log
from src.utils.error_handling import ErrorHandler


class UpdateProducts:
    """
    This class is used to update a product by id
    """
    def __init__(self, product):
        self.log = Log()
        self.product = product

    async def update_product(self):
        try:
            request = self.product
            url="http://ms-product:8000/api-products/delete-product/"
            params = request.model_dump()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    json=params,
                    headers={"Content-Type": "application/json"}
                )
            resp_data = response.json()
            self.log.logger.info(f"Products fetched successfully: {resp_data}")
            return resp_data
        except Exception as error:
            raise ErrorHandler.handle_error(error, "Error updating product")