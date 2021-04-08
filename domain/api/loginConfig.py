from flask_login import login_required, LoginManager, current_user, UserMixin
import requests
import config

loginManager=LoginManager()
current_user=current_user
login_required=login_required

class Tenant(UserMixin):
    def __init__(self, tenantName):
        super().__init__()
        self.tenantName=tenantName

@loginManager.user_loader
def user_loader(username):
    return None

@loginManager.request_loader
def request_loader(request):
    user=None
    if "Authorization" in request.headers:
        token = request.headers.get('Authorization')
        response=requests.get("http://"+str(config.IDP_IP)+":"+str(config.IDP_PORT)+str(config.IDP_ENDPOINT), headers={"Authorization":token})
        if response.status_code==200:
            data=response.json()
            user=Tenant(data["username"])
    return user