import json
import logging
import os
import uuid

from flask import Flask, g, request
from flask_cors import CORS

from database.database import Database
from controller import Controller
from settings import Settings
from utils.exceptions import IdentityProviderBaseException
from utils.time_logger import time_logger

flask_app = Flask(__name__)
CORS(flask_app)

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))
logger.debug('Logger configured')


class Router:
    def __init__(self, server: Flask):
        settings = Settings()
        database = Database()
        database.init_tokens_table()
        controller = Controller(settings, database=database)

        @server.after_request
        def after_request(res):
            print(f"Request path: {request.path}")
            if hasattr(g, 'token_uuid') and request.path == "/generate_token":
                print(f"Token UUID: {g.token_uuid}")
                controller.store_token(g.token_uuid)
            return res
        @server.route("/", methods=['GET', 'POST'])  # Index
        @time_logger
        def index():
            return {"message": "Index Called"}, 401

        @server.route('/generate_token', methods=['POST'])
        @time_logger
        def generate_token():
            g.token_uuid = controller.generate_token()
            return {"token": g.token_uuid}

        @server.route('/list_tokens', methods=['POST']) # Debug purposes only. Remove the endpoint in release
        @time_logger
        def list_tokens():
            tokens = database.list_tokens()
            return {"tokens in db": tokens}

        @server.route("/verify_token", methods=["GET"])
        @time_logger
        def verify_token():
            return {"Received token": controller.verify_token(request)}


        @server.errorhandler(Exception)
        def handle_identity_provider_exception(e):
            if issubclass(type(e), IdentityProviderBaseException):
                # start with the correct headers and status code from the error
                response = e.get_response()
                # replace the body with JSON
                response.data = json.dumps({
                    "code": e.code,
                    "name": e.__class__.__name__,
                    "description": e.description,
                })
                response.content_type = "application/json"
                return response

Router(flask_app)
if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8080, debug=True)
