import asyncio
from src.services.products_event_services import ProductsEventServices
from src.utils.logger_utils import Log


class EventHandler:
    def __init__(self):
        self.log = Log()
        self.products_event_service = ProductsEventServices()

    async def startup_event(self):
        self.log.logger.info("App iniciada, lanzando watcher de MongoDB")
        asyncio.create_task(self.products_event_service.watch_changes())


