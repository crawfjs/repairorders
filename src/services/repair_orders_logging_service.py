import logging
import logging.config
import os

class RepairOrdersLoggingService:
    def __init__(self, run_key: str):
        logging.config.fileConfig('audit_logging_config.ini')
        self.logger = logging.getLogger('RepairOrders')
        self.logger.propagate = False
        self.run_key = run_key

    def log(self, message: str):
        self.logger.info(f"{self.run_key} - {message}")

    def warn(self, message: str):
        self.logger.warn(f"{self.run_key} - {message}")

    def error(self, message: str):
        self.logger.error(f"{self.run_key} - {message}")
