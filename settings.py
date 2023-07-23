import logging
import os
from dataclasses import dataclass

@dataclass
class Settings:
    def __init__(self,
                 postgresqlHost: str = "postgres_db",
                 postgresqlDatabaseName: str = "postgres",
                 postgresqlUsername: str = "yildirimege",
                 postgresqlPassword: str = "123456",
                 postgresqlSSLMode: str = "require",
                 postgresqlConnectionPort : str = "5432"
                 ):

        self.postgreSqlHost = postgresqlHost or os.environ["POSTGRESQL_HOST"]
        self.postgresqlDatabaseName = postgresqlDatabaseName or os.environ["DATABASE_NAME"]
        self.postgresqlUsername = postgresqlUsername or os.environ["POSTGRESQL_USERNAME"]
        self.postgreSqlPassword = postgresqlPassword or os.environ["POSTGRESQL_PASSWORD"]
        self.postgresqlSSLMode = postgresqlSSLMode or os.environ["DB_SSL_MODE"]
        self.postgresqlConnectionPort = postgresqlConnectionPort or os.environ["DATABASE_CONN_PORT"]
    def log_config(self, log_level: str):
        logging.basicConfig(
            format='[%(levelname)s: %(asctime)s] %(module)s.%(funcName)s (line %(lineno)d): %(message)s', force=True)
        logger = logging.getLogger('logger1')
        logger.setLevel(log_level)
        logger.debug('Logger configured')
