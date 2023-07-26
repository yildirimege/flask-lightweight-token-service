import json
import unittest
import uuid
from datetime import datetime, timedelta
from unittest.mock import patch
import os
import sys
import inspect
from flask import Flask

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # Changing CWD to import
                                                                                         # classes without creating a package.
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from database.database import Database
from settings import Settings
from controller import Controller


class TokenAuthorizationTests(unittest.TestCase):
    test_db = Database()
    test_settings = Settings()

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.database = Database()
        self.settings = Settings()
        self.controller = Controller(self.database, self.settings)



    def test_valid_token(self):
        with patch('controller.get_token_timestamp') as mock_get_token_timestamp:
            # Simulate that the token is not expired (within 1 minute)
            mock_get_token_timestamp.return_value = datetime.utcnow() - timedelta(seconds=30)

            # Generate a valid token
            token = self.controller.generate_token()

            # Set the Authorization header with the token
            request_headers = {'Authorization': f'Bearer {token}'}

            # Send a GET request to the endpoint you want to test
            response = self.client.get('/verify_token', headers=request_headers)

            # Check the response status code and expected response content
            self.assertEqual(response.status_code, 200)
            expected_response = {"valid": True}
            self.assertEqual(json.loads(response.data), expected_response)

    def test_invalid_token(self):
        with patch('controller.get_token_timestamp') as mock_get_token_timestamp:
            # Simulate that the token is not expired (within 1 minute)
            mock_get_token_timestamp.return_value = datetime.utcnow() - timedelta(seconds=30)

            # Generate an invalid token (not in "Bearer xxx" format)
            token = "invalid_token"

            # Set the Authorization header with the invalid token
            request_headers = {'Authorization': token}

            # Send a GET request to the endpoint you want to test
            response = self.client.get('/verify_token', headers=request_headers)

            # Check the response status code and expected response content
            self.assertEqual(response.status_code, 200)
            expected_response = {"valid": False}
            self.assertEqual(json.loads(response.data), expected_response)

    def test_expired_token(self):
        with patch('controller.get_token_timestamp') as mock_get_token_timestamp:
            # Simulate that the token is expired (more than 1 minute old)
            mock_get_token_timestamp.return_value = datetime.utcnow() - timedelta(minutes=2)

            # Generate a valid token
            token = self.controller.generate_token()

            # Set the Authorization header with the token
            request_headers = {'Authorization': f'Bearer {token}'}

            # Send a GET request to the endpoint you want to test
            response = self.client.get('/verify_token', headers=request_headers)

            # Check the response status code and expected response content
            self.assertEqual(response.status_code, 200)
            expected_response = {"valid": False}
            self.assertEqual(json.loads(response.data), expected_response)


if __name__ == '__main__':
    unittest.main()
