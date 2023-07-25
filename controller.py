import logging
import os
import secrets
import uuid
from settings import Settings
from database.database import Database
from flask import request

from datetime import datetime, timedelta
from utils.utils import get_token_uuid_from_header

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))  # DEBUG by default.
logger.debug('Logger Configured.')


class Controller:

    def __init__(self, settings: Settings, database: Database):
        self.settings = settings
        self.database = database

    def is_request_valid(self, endpoint, received_request: request) -> bool:
        """
        Check if the incoming request body is valid for the given endpoint.

        Parameters:
        - endpoint (str): The name of the endpoint.
        - received_request (request): The incoming HTTP request object.

        Returns:
        - bool: True if the request body is valid, False otherwise.
        """

        if endpoint == 'verify_token':
            if endpoint == 'verify_token':
                # Check if the request has Authorization header
                if 'Authorization' not in received_request.headers:
                    return False

                # Check if the Authorization header follows the schema "Bearer xxx"
                auth_header = received_request.headers['Authorization']
                if not auth_header.startswith('Bearer '):
                    return False

                # Check if the UUID part after "Bearer " is a valid UUID
                token_uuid = auth_header.split('Bearer ')[1]
                try:
                    uuid.UUID(token_uuid)
                except ValueError:
                    return False

        # Add more conditions for other endpoints as needed

        # If the endpoint doesn't require any specific validation, return True
        return True

    def verify_token(self, received_request: request) -> bool:  # TODO: Refactor this.
        """
        Verify the validity of the provided token.

        Parameters:
            - received_request (request): The incoming HTTP request object.

        Returns:
            - bool: True if the token is valid and not expired, False otherwise.
        """
        token_uuid = get_token_uuid_from_header(received_request=received_request)
        token_timestamp = self.database.get_token_timestamp(token_uuid=token_uuid)

        time_difference = datetime.now() - token_timestamp

        return time_difference <= timedelta(seconds=60)

    def store_token(self, token_uuid):
        """
        Store the token in the database with its expiration timestamp.

        Parameters:
            - token_uuid (str): The UUID of the token to be stored.
        """
        self.database.store_token(token_uuid=token_uuid)
        logger.debug(
            f"Token with UUID '{token_uuid}' stored in the database at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    def generate_token(self):
        """
        Generate a new token.

        Returns:
            - str: The generated token uuid (version 4).
        """
        token = str(uuid.uuid4())
        logger.debug(f"New token generated with UUID: {token} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return token
