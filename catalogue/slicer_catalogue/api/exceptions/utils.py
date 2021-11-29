import re
from werkzeug.exceptions import HTTPException
from api.views.utils import response_template
from http import HTTPStatus


def handle_exception(app):
    @app.errorhandler(Exception)
    def decorator(e):
        if isinstance(e, Exception):  # Ignore startup call
            if isinstance(e, HTTPException):  # If it is a Http Error
                return response_template(message=e.description, status_code=e.code)

            # If it is a python Error
            return response_template(message=f'Internal exception - {e}', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    return decorator


def exception_message_elements(cls, **kwargs):
    """
    @param cls: Class object
    @param kwargs: Query's arguments
    @return: a tuple with the class name and concatenation of args in string
    """
    class_name = ' '.join(re.findall('[A-Z][^A-Z]*', cls.__name__))

    args = []
    for arg_name, arg_value in kwargs.items():
        args += [f"{arg_name} {str(arg_value)}"]
    
    return class_name, ", ".join(args)
