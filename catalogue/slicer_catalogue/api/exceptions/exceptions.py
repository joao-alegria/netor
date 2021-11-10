from werkzeug.exceptions import HTTPException
from http import HTTPStatus


class MalFormedException(HTTPException):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self, description='Malformed request'):
        self.description = description


class FailedOperationException(HTTPException):

    def __init__(self, description, code=HTTPStatus.CONFLICT):
        self.description = description
        self.code = code


class BadVsBlueprintBody(HTTPException):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self, description):
        self.description = description


class AlreadyExistingEntityException(HTTPException):
    code = HTTPStatus.CONFLICT

    def __init__(self, description):
        self.description = description


class NotFoundException(HTTPException):
    code = HTTPStatus.NOT_FOUND

    def __init__(self, description):
        self.description = description


class MalformedTarFileException(HTTPException):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self, description):
        self.description = description


class IllegalStateException(HTTPException):
    code = HTTPStatus.CONFLICT

    def __init__(self, description):
        self.description = description


class InvalidEntity(HTTPException):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self, description):
        self.description = description


class NotExistingEntityException(HTTPException):
    code = HTTPStatus.NOT_FOUND

    def __init__(self, description):
        self.description = description
