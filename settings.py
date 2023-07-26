import logging
import os
from dataclasses import dataclass


@dataclass
class Settings:
    def __init__(self):
        self.postgresql_username = os.environ["POSTGRESQL_USERNAME"]
        self.postgresql_password = os.environ["POSTGRESQL_PASSWORD"]
        self.postgresql_database_name = os.environ["POSTGRESQL_DB_NAME"]
        self.postgresql_host = os.environ["POSTGRESQL_HOST"]
        self.postgresql_connection_port = os.environ["POSTGRESQL_DB_PORT"]
        self.token_expiration_time: int = int(os.environ["TOKEN_EXPIRATION_TIME"])
        self.token_clearer_frequency: int = int(os.environ["TOKEN_CLEAR_FREQUENCY"])
        self.postgresql_ssl_mode = os.environ["POSTGRESQL_SSL_MODE"]

    def log_config(self, log_level: str):
        logging.basicConfig(
            format='[%(levelname)s: %(asctime)s] %(module)s.%(funcName)s (line %(lineno)d): %(message)s', force=True)
        logger = logging.getLogger('logger1')
        logger.setLevel(log_level)
        logger.debug('Logger configured')
