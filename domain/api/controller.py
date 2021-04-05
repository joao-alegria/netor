from flask import Flask, jsonify, request
from flasgger import Swagger, validate
import service as domainService
from api.loginConfig import loginManager, login_required

app = Flask(__name__)

swagger_config = {
    "openapi": "3.0.3",
    "title": "Domain Management API",
    "swagger_ui": True,
}

swagger = Swagger(app, config=swagger_config, merge=True,template_file='definitions.yaml')

loginManager.init_app(app)

@app.route('/domain', methods=["GET"])
@login_required
def getAllDomains():
    """
    Return all the Domains in the system
    ---
    responses:
        200:
            description: returns a list of all the domains
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: '#/definitions/Domain'
    """

    return jsonify(domainService.getAllDomains())

@app.route('/domain', methods=["POST"])
@login_required
def createNewDomain():
    """
    Creates a new Domain
    ---
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/definitions/Domain'
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
    validate(data, 'Domain', 'definitions.yaml')

    # response = vsService.createNewVS(data)

    return jsonify(domainService.createDomain())

@app.route('/domain/<domainId>', methods=["GET"])
@login_required
def getDomainById(domainId):
    """
    Returns the Domain requested
    ---
    responses:
        200:
            description: returns the domain indicated
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Domain'
    """
    return jsonify(domainService.getDomain(domainId))

@app.route('/domain/<domainId>', methods=["PUT"])
@login_required
def updateDomain(domainId):
    """
    Updates the Domain indicated
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    return jsonify(domainService.updateDomain(domainId))

@app.route('/domain/<domainId>', methods=["DELETE"])
@login_required
def removeDomain(domainId):
    """
    Remove and deletes the Domain indicated
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    return jsonify(domainService.removeDomain(domainId))