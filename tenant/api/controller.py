from flask import g, Flask, jsonify, render_template, request, make_response, redirect
from flasgger import Swagger, validate
from flasgger.utils import swag_from
from db.persistance import Tenant, OauthClient, session
from api.oauth import OauthProvider
import service
from api.loginConfig import loginManager, loginUser

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "openapi": "3.0.3",
    "title": "Tenant and Group Service API",
    "version": '',
    "termsOfService": "",
    "swagger_ui": True,
    "description": "",
}
swagger = Swagger(app, config=swagger_config, merge=True,template_file='definitions.yaml')

oauth = OauthProvider(app)

loginManager.init_app(app)

#---------------------LOGIN----------------------------

@app.route('/login', methods=['GET','POST'])
def home():
    if request.method=='GET':
        return render_template('index.html')
    
    username = request.form.get('username')
    user = session.query(Tenant).filter(Tenant.username==username).first()
    if user.check_password(request.form['password']):
        loginUser(user)
        return redirect("/protected")

#---------------OAUTH2-------------------------------

@app.before_request
def load_current_user():
    if "client_id" in request.args:
        clientId=request.args.get("client_id")
        client = session.query(OauthClient).filter(OauthClient.client_id==clientId).first()
        g.client = client
    # if "username" in request.args:
    #     username=request.args.get("username")
    user = session.query(Tenant).first()
    g.user = user

@app.route('/oauth/authorize', methods=['GET', 'POST'])
# @login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    # NOTICE: for real project, you need to require login
    if request.method == 'GET':
        # render a page for user to confirm the authorization
        return render_template('consent.html')

    if request.method == 'HEAD':
        # if HEAD is supported properly, request parameters like
        # client_id should be validated the same way as for 'GET'
        response = make_response('', 200)
        response.headers['X-Client-ID'] = kwargs.get('client_id')
        return response

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'

@app.route('/oauth/token', methods=['POST', 'GET'])
# @login_required
@oauth.token_handler
def access_token():
    return {}

@app.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    pass

@app.route('/validate')
@oauth.require_oauth()
def validateToken():
    return jsonify(msg="Valid"), 200

@oauth.invalid_response
def require_oauth_invalid(req):
    return jsonify(message=req.error_message), 401


#-----------------TENANT API---------------------------

@app.route('/group', methods=["GET"])
@oauth.require_oauth()
def getAllGroups():
    """
    Return all the Groups in the system
    ---
    responses:
        200:
            description: returns a list with all the groups in the system
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: '#/definitions/Group'
    """
    return service.getAllGroups()

@app.route('/group', methods=["POST"])
@oauth.require_oauth()
def createNewGroup():
    """
    Creates a new Group
    ---
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/definitions/Group'
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
    validate(data, 'Group', 'definitions.yaml')

    return service.createGroup(request.oauth.user.username,data)

@app.route('/group/<groupId>', methods=["GET"])
@oauth.require_oauth()
def getGroupById(groupId):
    """
    Returns the Group requested
    ---
    responses:
        200:
            description: returns the group indicated
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Group'
    """
    return service.getGroupById(groupId)

@app.route('/group/<groupId>', methods=["PUT"])
@oauth.require_oauth()
def modifyGroup(groupId):
    """
    Modifies the Group indicated
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    return service.modifyGroup(groupId)

@app.route('/group/<groupId>', methods=["DELETE"])
@oauth.require_oauth()
def removeGroup(groupId):
    """
    Deletes the Group indicated and the attached tenants
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    return service.removeGroup(groupId)

@app.route('/tenant', methods=["GET"])
@oauth.require_oauth()
def getAllTenants():
    """
    Return all the Tenants in the system
    ---
    responses:
        200:
            description: returns a list with all the tenants in the system
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: '#/definitions/Tenant'
    """
    return service.getAllTenants()

@app.route('/tenant', methods=["POST"])
@oauth.require_oauth()
def createNewTenant():
    """
    Creates a new Tenant
    ---
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/definitions/Tenant'
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
    validate(data, 'Tenant', 'definitions.yaml')

    return service.createTenant(request.oauth.user.username,data)

@app.route('/tenant/<tenantId>', methods=["GET"])
@oauth.require_oauth()
def getTenantById(tenantId):
    """
    Returns the Tenant requested
    ---
    responses:
        200:
            description: returns the tenant indicated
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Tenant'
    """
    return service.getTenantById(tenantId)

@app.route('/tenant/<tenantId>', methods=["PUT"])
@oauth.require_oauth()
def modifyTenant(tenantId):
    """
    Modifies the Tenant indicated
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    return service.modifyTenant(tenantId)

@app.route('/tenant/<tenantId>', methods=["DELETE"])
@oauth.require_oauth()
def removeTenant(tenantId):
    """
    Deletes the Tenant indicated and the attached tenants
    ---
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    return service.removeTenant(tenantId)
