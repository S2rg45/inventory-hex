import traceback
from fastapi import HTTPException
from typing import Any, Dict, List, Union
from .logger_utils import Log


log = Log()

class ErrorHandler:
    @staticmethod
    def handle_error(error: Exception, message: str = "An error occurred"):
        """
        Handle errors by logging them and raising an HTTPException.
        :param error: The exception that occurred.
        :param message: A custom message to log.
        """
        log.logger.error(f"{message}: {str(error)}")
        log.logger.error(f"Error trace: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error)) from error
    

    @staticmethod
    def handle_validation_error(error: Exception, message: str = "Validation error occurred"):
        """
        Handle validation errors by logging them and raising an HTTPException.
        :param error: The validation exception that occurred.
        :param message: A custom message to log.
        """
        log.logger.error(f"{message}: {str(error)}")
        log.logger.error(f"Error trace: {traceback.format_exc()}")
        raise HTTPException(status_code=422, detail=str(error)) from error
    

    @staticmethod
    def handle_not_found_error(resource: str, resource_id: Union[str, int], message: str = "Resource not found"):
        """
        Handle not found errors by logging them and raising an HTTPException.
        :param resource: The type of resource that was not found.
        :param resource_id: The ID of the resource that was not found.
        :param message: A custom message to log.
        """
        log.logger.error(f"{message}: {resource} with ID {resource_id} not found")
        raise HTTPException(status_code=404, detail=f"{resource} with ID {resource_id} not found")
    

    @staticmethod
    def handle_service_unavailable(message: str = "Service is currently unavailable"):
        """
        Handle service unavailable errors by logging them and raising an HTTPException.
        :param message: A custom message to log.
        """
        log.logger.error(message)
        raise HTTPException(status_code=503, detail=message)
    

    @staticmethod
    def handle_request_timeout(message: str = "Request timed out"):
        """
        Handle request timeout errors by logging them and raising an HTTPException.
        :param message: A custom message to log.
        """
        log.logger.error(message)
        raise HTTPException(status_code=408, detail=message)
    
