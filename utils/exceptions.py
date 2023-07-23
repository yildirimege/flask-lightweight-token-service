from werkzeug.exceptions import HTTPException


class IdentityProviderBaseException(HTTPException):
    """
    Any exceptions that we can safely return to the client will derive from this one
    """
    code = 400


class TokenExpiredError(IdentityProviderBaseException):
    code = 404
    description = 'Token is Expired.'


class InvalidTokenError(IdentityProviderBaseException):
    code = 404
    description = "Token is Invalid."
