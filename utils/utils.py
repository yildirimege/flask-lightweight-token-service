from flask import request


def get_token_uuid_from_header(received_request: request):
    authorization_header = received_request.headers.get('Authorization')

    if authorization_header and authorization_header.startswith('Bearer '):
        return authorization_header.split(' ')[1]
