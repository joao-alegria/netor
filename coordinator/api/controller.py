from flask import Flask, jsonify, request
from flasgger import Swagger, validate
import service as vsService
from api.loginConfig import loginManager, current_user, login_required
from flask_cors import CORS, cross_origin

app = Flask(__name__)
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
        return jsonify({"message":"Success", "data":vsis}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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
        vsiId=vsService.createNewVS(current_user.name,data)
        return jsonify({"message":"Success", "data":{"vsiId":vsiId}}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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
        return jsonify({"message":"Success", "data":vsi}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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
        return jsonify({"message":"Success"}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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
        message=vsService.removeVSI(current_user.name, vsiId)
        return jsonify({"message":message}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500