import json
import logging
import os
import uuid

from flask import Flask, g, request, jsonify
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

        @server.before_request
        def validate_request_body():
            """
            Validate the incoming request body for each endpoint.

            If the request body is not valid, return an error response.
            """
            endpoint = request.endpoint
            valid = controller.is_request_valid(endpoint, request)

            if not valid:
                response = jsonify({"error": "Invalid request. Your Request must have Authorization layer in a "
                                             "specific format. (Check the docs)"})
                response.status_code = 400
                return response
        @server.after_request
        def after_request(res):
            """
            Log the token UUID to the database after processing the request.

            Parameters:
                - res (response): The HTTP response object.

            Returns:
                - response: The modified HTTP response object.
            """
            if hasattr(g, 'token_uuid') and request.path == "/generate_token":
                controller.store_token(g.token_uuid)
            else:
                pass
            return res

        @server.route("/", methods=['GET', 'POST'])  # Index
        @time_logger
        def index():
            """
            The index route. Returns a message and a status code 401.

            Returns:
                - dict: A JSON object with the message and status code.
            """
            return {"message": "Please enter a valid URL."}, 401

        @server.route('/generate_token', methods=['POST'])
        @time_logger
        def generate_token():
            """
            The endpoint to generate a new token.

            Returns:
                - dict: A JSON object with the generated token.
            """
            g.token_uuid = controller.generate_token()
            return {"token": g.token_uuid}

        @server.route("/verify_token", methods=["GET"])
        @time_logger
        def verify_token():
            """
            The endpoint to verify the validity of the provided token.

            Returns:
                - dict: A JSON object indicating if the token is valid.
            """
            return {"valid": controller.verify_token(request)}

        @server.errorhandler(Exception)
        def handle_identity_provider_exception(e):
            """
            Error handler for IdentityProviderBaseException and its subclasses.

            Parameters:
                - e (Exception): The caught exception.

            Returns:
                - response: The HTTP response object with the error details.
            """
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
