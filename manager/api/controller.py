from flask import Flask, jsonify, request
from flasgger import Swagger, validate, LazyString
from manager import getCSMF
from flask_cors import CORS, cross_origin
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
    app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/manager')

CORS(app)

swagger_config = {
    "openapi": "3.0.3",
    "title": "Interdomain NetOr(Network Orchestrator) API",
    "swagger_ui": True,
}
#template = dict(swaggerUiPrefix=LazyString(lambda : request.environ.get('HTTP_X_SCRIPT_NAME', '')))
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