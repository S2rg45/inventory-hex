
from fastapi import Header, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import JSONResponse

import urllib.request
import json
import traceback

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
            req = urllib.request.Request(
                url="http://localhost:8000/api-products/delete-product/",
                data=json.dumps(self.product).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req) as resp:
                resp_data = json.loads(resp.read().decode())
            # Return only the data, not a JSONResponse
            return resp_data
        except Exception as error:
            raise ErrorHandler.handle_error(error, "Error updating product")