

from fastapi import Header, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import JSONResponse

import urllib.request
import json
import traceback

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
            req = urllib.request.Request(
                url="http://localhost:8000/api-products/product/",
                data=json.dumps(self.product_id.model_dump()).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req) as resp:
                resp_data = json.loads(resp.read().decode())
            self.log.logger.info(f"Products fetched successfully: {resp_data}")
            # Return only the data, not a JSONResponse
            return resp_data
        except Exception as error:
            raise ErrorHandler.handle_error(error, "Error fetching products")
        

    