from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# Importing routes

from src.services.products_services import router
from src.utils.events import EventHandler
from src.utils.logger_utils import Log

log = Log()
# Creating FastAPI instance
app = FastAPI(title="Api Products", 
              description="API for Products", 
              version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# Including routes
app.include_router(router)
app.add_event_handler("startup", EventHandler().startup_event)                    


# Running server
log.logger.info("server running")
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

