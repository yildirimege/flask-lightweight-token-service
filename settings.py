import logging
import os
from dataclasses import dataclass


@dataclass
class Settings:
    def __init__(self,
                 postgresql_host: str = "postgres_db",
                 postgresql_database_name: str = "postgres",
                 postgresql_username: str = "yildirimege",
                 postgresql_password: str = "123456",
                 postgresql_ssl_mode: str = "require",
                 postgresql_connection_port: str = "5432"
                 ):
        self.postgresql_host = postgresql_host or os.environ["POSTGRESQL_HOST"]
        self.postgresql_database_name = postgresql_database_name or os.environ["DATABASE_NAME"]
        self.postgresql_username = postgresql_username or os.environ["POSTGRESQL_USERNAME"]
        self.postgresql_password = postgresql_password or os.environ["POSTGRESQL_PASSWORD"]
        self.postgresql_ssl_mode = postgresql_ssl_mode or os.environ["DB_SSL_MODE"]
        self.postgresql_connection_port = postgresql_connection_port or os.environ["DATABASE_CONN_PORT"]

    def log_config(self, log_level: str):
        logging.basicConfig(
            format='[%(levelname)s: %(asctime)s] %(module)s.%(funcName)s (line %(lineno)d): %(message)s', force=True)
        logger = logging.getLogger('logger1')
        logger.setLevel(log_level)
        logger.debug('Logger configured')
