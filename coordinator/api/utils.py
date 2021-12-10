from flask import jsonify,make_response
def prepare_response(message="",data=[],status_code=200):
    response_content = jsonify({'message': message, 'data':data})
    return make_response(response_content, status_code)