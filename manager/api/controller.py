from flask import Flask, jsonify, request
from flasgger import Swagger, validate
import manager

app = Flask(__name__)

swagger_config = {
    "openapi": "3.0.3",
    "title": "Interdomain NetOr(Network Orchestrator) API",
    "swagger_ui": True,
}

swagger = Swagger(app, config=swagger_config, merge=True,template_file='definitions.yaml')


@app.route('/interdomain', methods=["POST"])
def getAllDomains():
    """
    Receives VNF information to establish the interdomain tunnel
    ---
    responses:
        200:
            description: acknowledges
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """

    data=request.json

    return jsonify(manager.newVnfInfo(data))