from flask_login import login_required, LoginManager, login_user, logout_user, current_user,AnonymousUserMixin
import base64
from flask import jsonify
from db.persistance import Tenant, OauthClient, DB

loginManager=LoginManager()

@loginManager.user_loader
def user_loader(username):
    user = DB.session.query(Tenant).filter(Tenant.username==username).first()
    g.user=user
    return user

@loginManager.request_loader
def request_loader(request):
    user=None
    if "username" in request.form:
        username = request.form.get('username')
        if username != None:
            user = DB.session.query(Tenant).filter(Tenant.username==username).first()
    
    if "Basic" in request.headers:
        header_val = request.headers.get('Authorization').replace('Basic ', '', 1)
        try:
            header_val = base64.b64decode(header_val)
            data=header_val.decode("utf-8").split(":")
            user=DB.session.query(Tenant).filter(Tenant.username==data[0]).first()
        except TypeError:
            pass
    g.user=user
    return user

@loginManager.unauthorized_handler
def unauthorized():
    # do stuff
    return jsonify({"msg":"Unauthorized user"}), 401

def loginUser(user):
    login_user(user,remember=True)