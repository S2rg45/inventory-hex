import structlog


class Log:
    
    def __init__(self):
        self.structlog = structlog.get_logger()
        self.logger = self.structlog
        
