from fastapi import Header, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

import asyncio



from src.repository.products_repository import ProductsRepository
from src.utils.logger_utils import Log
from src.utils.error_handling import ErrorHandler


class ProductsEventServices:
    """
    This class is used to handle events related to products.
    It listens for changes in the products collection and processes them accordingly.
    """

    def __init__(self):
        self.log = Log()

    async def watch_changes(self):
        try:
            self.log.logger.info("Starting to watch changes in products collection")
            collection = ProductsRepository().get_collection()
            async with collection.watch() as stream:
                async for change in stream:
                    self.log.logger.info(f"Change detected: {change}")
                    # Here you can add logic to handle the change, e.g., update a cache or notify users
        except Exception as e:
            self.log.logger.error(f"Error watching changes: {str(e)}")
            raise HTTPException(status_code=500, detail="Error watching changes")


