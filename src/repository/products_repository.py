from motor.motor_asyncio import AsyncIOMotorClient
from src.utils.settings import config


class ProductsRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(config["local"]["connection"])
        self.db = self.client[config["local"]["db"]]
        self.collection_name = config["local"]["collection_owner"]

    def get_collection(self):
        return self.db[self.collection_name]


