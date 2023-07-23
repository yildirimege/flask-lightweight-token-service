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

    def verify_token(self, received_request: request) -> bool:  # TODO: Refactor this.
        token_uuid = get_token_uuid_from_header(received_request=received_request)
        token_timestamp = self.database.get_token_timestamp(token_uuid=token_uuid)

        time_difference = datetime.now() - token_timestamp

        return time_difference <= timedelta(seconds=60)

    def store_token(self, token_uuid):
        self.database.store_token(token_uuid=token_uuid)

    def generate_token(self):
        token = str(uuid.uuid4())
        return token
