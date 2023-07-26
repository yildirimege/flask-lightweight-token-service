import os
import psycopg2
import logging
from datetime import datetime, timedelta
from settings import Settings
import time

settings = Settings()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

token_clear_frequency = int(os.environ.get('TOKEN_CLEAR_FREQUENCY', 300))


class TokenClearer:

    def __init__(self):
        self.host = settings.postgresql_host
        self.port = settings.postgresql_connection_port
        self.databaseName = settings.postgresql_database_name
        self.user = settings.postgresql_username
        self.password = settings.postgresql_password

        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.databaseName,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            logger.info("Connected to Database!")

        except psycopg2.Error as e:
            logger.error(f"Error connecting to DB: {e}")

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            logger.info("Disconnected from DB.")
        else:
            logger.error("Error while disconnecting from DB.")

    def clear_expired_tokens(self):
        current_time = datetime.now()
        delete_query = "DELETE FROM token_table WHERE expiration_time < %s;"
        self.cursor.execute(delete_query, (current_time,))
        self.connection.commit()
        logger.info(f"Expired tokens cleared from the database at {current_time.strftime('%Y-%m-%d %H:%M:%S')}.")


if __name__ == '__main__':
    clearer = TokenClearer()
    while True:
        # Clear expired tokens from the database
        clearer.clear_expired_tokens()

        # Wait for the specified frequency
        time.sleep(token_clear_frequency)
