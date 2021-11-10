from http import HTTPStatus


def response_template(message, data=None, status_code=HTTPStatus.OK):
    if data is None:
        data = []
    return {
        'message': message,
        'data': data
    }, status_code
