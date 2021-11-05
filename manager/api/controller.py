from flask import Flask, jsonify, request
from flasgger import Swagger, validate
from manager import getCSMF
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

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
    csmf=getCSMF(data["vsiId"])
    if csmf:
        return jsonify(csmf.interdomainHandler(data))
    else:
        return "VSI Id not found", 500