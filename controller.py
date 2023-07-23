import logging
import os
import secrets
import uuid
from settings import Settings
from database.database import Database
from flask import request

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))  # DEBUG by default.
logger.debug('Logger Configured.')


class Controller:

    def __init__(self, settings: Settings, database: Database):
        self.settings = settings
        self.database = database

    def verify_token(self, received_request: request) -> bool:  # TODO: Refactor this.
        authorization_header = received_request.headers.get('Authorization')

        if authorization_header and authorization_header.startswith('Bearer '):
            token_uuid = authorization_header.split(' ')[1]
            token_timestamp = self.database.get_token_timestamp(token_uuid=token_uuid)

            current_time = datetime.now()
            time_difference = current_time - token_timestamp

            return time_difference <= timedelta(seconds=60)

    def store_token(self, token_uuid):
        self.database.store_token(token_uuid=token_uuid)

    def generate_token(self):
        token = str(uuid.uuid4())
        return token
