from flask import g, Flask, jsonify, render_template, request, make_response, redirect
from flasgger import Swagger, validate
from flasgger.utils import swag_from
from db.persistance import Tenant, OauthClient, DB, OauthToken
from api.oauth import OauthProvider
import service
from api.loginConfig import loginManager, loginUser
from flask_cors import CORS, cross_origin
import logging
from api.utils import prepare_response

app = Flask(__name__)
CORS(app)

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
def login():
    if request.method=='GET':
        return render_template('index.html')
    
    username = request.form.get('username')
    user = DB.session.query(Tenant).filter(Tenant.username==username).first()
    if user.check_password(request.form['password']):
        loginUser(user)
        return redirect("/protected")

#---------------OAUTH2-------------------------------

@app.before_request
def load_current_user():
    if "client_id" in request.args:
        clientId=request.args.get("client_id")
        client = DB.session.query(OauthClient).filter(OauthClient.client_id==clientId).first()
        g.client = client
    # if "username" in request.args:
    #     username=request.args.get("username")

    if "Authorization" in request.headers:
        token=request.headers["Authorization"].replace("Bearer ","")
        token=DB.session.query(OauthToken).filter(OauthToken.access_token==token).first()
        if token:
            g.user = token.user
        else:
            g.user = None
    else:
        g.user=None


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
    try:
        tenant=service.getTenantById(request.oauth.user.username)
        return prepare_response(message="Success",data=tenant)
    except Exception as e:
        return prepare_response(message=f"Error: {e}", status_code=403)

@oauth.invalid_response
def require_oauth_invalid(req):
    try:
        return prepare_response(message=req.error_message,status_code= 401)
    except Exception as e:
        return prepare_response(message=f"Error: {e}",status_code=500)


#-----------------TENANT API---------------------------

@app.route('/group', methods=["GET"])
@oauth.require_oauth()
def getAllGroups():
    """
    Return all the Groups in the system
    ---
    tags:
      - groups
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
    try:
        groups=service.getAllGroups()
        return prepare_response(message="Success getting all Groups",data=groups)
    except Exception as e:
        return prepare_response(message=f"Error getting all Groups: {e}",status_code=400)

@app.route('/group', methods=["POST"])
@oauth.require_oauth()
def createNewGroup():
    """
    Creates a new Group
    ---
    tags:
      - groups
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
    try:
        group = service.createGroup(request.oauth.user.username,data)
        return prepare_response(message="Success creating new Group", data=group)
    except Exception as e:
        message = f"Error creating new Group: {e.message}"
        return prepare_response(message=message,status_code=e.status_code)

@app.route('/group/<groupId>', methods=["GET"])
@oauth.require_oauth()
def getGroupById(groupId):
    """
    Returns the Group requested
    ---
    tags:
      - groups
    responses:
        200:
            description: returns the group indicated
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Group'
    """
    try:
        group=service.getGroupById(groupId)
        if not group:
            return prepare_response(message=f"Could not find group with id {groupId}", status_code=404)
        return prepare_response(message="Success", data=group)
    except Exception as e:
        message = f"Error obtaining Group with id {groupId}: {e}"
        return prepare_response(message=message, status_code=400)

@app.route('/group/<groupId>', methods=["PUT"])
@oauth.require_oauth()
def modifyGroup(groupId):
    """
    Modifies the Group indicated
    ---
    tags:
      - groups
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    try:
        service.modifyGroup(groupId)
        return jsonify({"message":"Success"}),200
    except Exception as e:
        message = f"Error modifying Group with id {groupId}: {e}"
        return prepare_response(message=message, status_code=400)

@app.route('/group/<groupId>', methods=["DELETE"])
@oauth.require_oauth()
def removeGroup(groupId):
    """
    Deletes the Group indicated and the attached tenants
    ---
    tags:
      - groups
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    try:
        service.removeGroup(groupId)
        return jsonify({"message":"Success"}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

@app.route('/tenant', methods=["GET"])
@oauth.require_oauth()
def getAllTenants():
    """
    Return all the Tenants in the system
    ---
    tags:
      - tenants
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
    try:
        tenants=service.getAllTenants()
        return jsonify({"message":"Success", "data":tenants}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

@app.route('/tenant', methods=["POST"])
@oauth.require_oauth()
def createNewTenant():
    """
    Creates a new Tenant
    ---
    tags:
      - tenants
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
    try:
        service.createTenant(request.oauth.user.username,data)
        return jsonify({"message":"Success"}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

@app.route('/tenant/<tenantId>', methods=["GET"])
@oauth.require_oauth()
def getTenantById(tenantId):
    """
    Returns the Tenant requested
    ---
    tags:
      - tenants
    responses:
        200:
            description: returns the tenant indicated
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Tenant'
    """
    try:
        tenant=service.getTenantById(tenantId)
        return jsonify({"message":"Success", "data":tenant}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

@app.route('/tenant/<tenantId>', methods=["PUT"])
@oauth.require_oauth()
def modifyTenant(tenantId):
    """
    Modifies the Tenant indicated
    ---
    tags:
      - tenant
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    try:
        service.modifyTenant(tenantId)
        return jsonify({"message":"Success"}),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500

@app.route('/tenant/<tenantId>', methods=["DELETE"])
@oauth.require_oauth()
def removeTenant(tenantId):
    """
    Deletes the Tenant indicated and the attached tenants
    ---
    tags:
      - tenant
    responses:
        200:
            description: acknowledges the request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Acknowledge'
    """
    try:
        return jsonify(service.removeTenant(tenantId)),200
    except Exception as e:
        return jsonify({"message":"Error: "+str(e)}),500