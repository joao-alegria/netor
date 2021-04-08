from flask import Flask, jsonify, request
from flasgger import Swagger, validate
import db.persistance
import service as vsService
from api.loginConfig import loginManager, current_user, login_required

app = Flask(__name__)

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

    return jsonify(vsService.getAllVSIs(current_user.tenantName))

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

    return jsonify(vsService.createNewVS(current_user.tenantName,data))

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

    return jsonify(vsService.getVSI(current_user.tenantName, vsiId))

@app.route('/vs/<vsiId>', methods=["PUT"])
@login_required
def modifyVs(vsiId):
    """
    Modifies or terminates the Vertical Service indicated
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """

    return jsonify(vsService.modifyVSI(current_user.tenantName, vsiId))

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

    return jsonify(vsService.removeVSI(current_user.tenantName, vsiId))