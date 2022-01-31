from flask import Flask, jsonify, request
from flasgger import Swagger, validate
import service as domainService
from api.loginConfig import loginManager, login_required
from flask_cors import CORS, cross_origin
import requests
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
    app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/domain')
CORS(app)

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

    try:
        domains=domainService.getAllDomains()
        return jsonify({"message":"Success", "data":domains}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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

    # check if domain already exists in db
    db_domain = domainService.getOsmDomain(data['ownedLayers'][0]['domainLayerId'])
    if db_domain:
        if(db_domain['username'] == data['ownedLayers'][0]['username'] and db_domain['password'] == data['ownedLayers'][0]['password']\
        and db_domain['project'] == data['ownedLayers'][0]['project']):
            return jsonify({"message":f"Error: domain with Id {data['ownedLayers'][0]['domainLayerId']} already exists"}),409

    try:
        r = requests.post(f"{data['url']}/osm/admin/v1/tokens", data = {"username": data['ownedLayers'][0]['username'], \
            "password": data['ownedLayers'][0]['password'], "project_id": data['ownedLayers'][0]['project']}, timeout=15)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        return jsonify({'message': f"Error: Could not connect to {data['url']}"}),400
    except Exception as e:
        return jsonify({"message":f"Error: {e}"}),400

    try:
        domainService.createDomain(data)
        return jsonify({"message":"Success"}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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

    try:
        domain=domainService.getDomain(domainId)
        return jsonify({"message":"Success", "data":domain}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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

    try:
        domainService.updateDomain(domainId)
        return jsonify({"message":"Success"}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

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

    try:
        domainService.removeDomain(domainId)
        return jsonify({"message":"Success"}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500
