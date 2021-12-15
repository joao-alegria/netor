from flask import Flask, jsonify, request
from flask.helpers import make_response
from flasgger import Swagger, validate
import service as vsService
from api.loginConfig import loginManager, current_user, login_required
from flask_cors import CORS, cross_origin
from api.utils import prepare_response
import config

class ReverseProxied(object):
    def __init__(self, app, script_name):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.script_name
        return self.app(environ, start_response)


app = Flask(__name__)
if config.ENVIRONMENT != 'testing':
    app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/lcm')
CORS(app)

swagger_config = {
    "openapi": "3.0.3",
    "title": "VS LCM API",
    "swagger_ui": True,
}

swagger = Swagger(app, config=swagger_config, merge=True,template_file='definitions.yaml')

loginManager.init_app(app)


@app.route('/vs', methods=["GET"])
@login_required
def getAllVSs():
    """
    Return all the Vertical Services in the system
    ---
    responses:
        200:
            description: returns a list of all the vertical slicers
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: '#/definitions/VS'
    """
    try:
        vsis=vsService.getAllVSIs(current_user.name)
        return prepare_response(message='Success obtaining all VSs', data=vsis)
    except Exception as e:
        message = f"Error obtaining all Vertical Services: {e}"
        return prepare_response(message=message,status_code=400)

@app.route('/vs', methods=["POST"])
@login_required
def createNewVS():
    """
    Creates a new Vertical Service
    ---
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/definitions/VS'
        required: true
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """

    data=request.json
    validate(data, 'VS', 'definitions.yaml')
    try:
        vsi=vsService.createNewVS(current_user.token,current_user.name,data)

        return prepare_response(message="Success creating new VS", data=vsi)
    except Exception as e:
        message = f"Error creating new VS: {e.message}"
        return prepare_response(message=message, status_code=e.status_code)

@app.route('/vs/<vsiId>', methods=["GET"])
@login_required
def getVSById(vsiId):
    """
    Returns the Vertical Service requested
    ---
    responses:
        200:
            description: returns the vertical service indicated
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/VS'
    """

    try:

        vsi=vsService.getVSI(current_user.name, vsiId)
        if not vsi:
            return prepare_response(message=f"VS With Id {vsiId} does not exist", status_code=404)
        return prepare_response(message="Success Getting VS",data=vsi)
        
    except Exception as e:
        message = f'Error getting VS: {e}'
        return prepare_response(message=message,status_code=400)

@app.route('/vs/<vsiId>', methods=["PUT"])
@login_required
def modifyVs(vsiId):
    """
    Modifies/terminates/sendAction the Vertical Service indicated
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """

    try:
        data=request.json
        vsService.modifyVSI(current_user.name, vsiId, data)
        return prepare_response(message=f"Sucess updating VS with Id {vsiId}")
    except Exception as e:
        message = f"Error Updating VS With Id {vsiId}: {e}"
        return prepare_response(message=message, status_code=400)

@app.route('/vs/<vsiId>', methods=["DELETE"])
@login_required
def removeVs(vsiId):
    """
    Remove and deletes the Vertical Service indicated
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """

    try:
        force=request.args.get("force")
        message=vsService.removeVSI(current_user.name, vsiId, force=force)
        return prepare_response(message=message)
    except Exception as e:
        message = f'Error deleting VS with Id {vsiId}: {e}'
        return prepare_response(message=message,status_code=400)


@app.route('/vs/<vsiId>/status')
def getVSiStatusHistory(vsiId):
    """
    Returns All Status that a Vertical Slice has been through
    ---
    responses:
        200:
            description: Returns All Status that a Vertical Slice has been through
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: '#/definitions/VS'
    """
    try:
        vsiStatus = vsService.getAllVSIStatus(current_user.name,vsiId)
        return prepare_response(message=f'Success obtaining all Status for VSi {vsiId}', data=vsiStatus)
    except Exception as e:
        message = f'Error getting VS Status: {e.message}'
        return prepare_response(message=message,status_code=e.status_code)
