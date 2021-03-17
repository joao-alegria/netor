from flask_login import login_required, LoginManager, current_user, UserMixin
import requests

loginManager=LoginManager()
current_user=current_user

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
        response=requests.get("http://localhost:5002/validate", headers={"Authorization":token})
        if response.status_code==200:
            # userInfo=requests.get("http://localhost:5002/tenant", headers={"Authorization":token})
            user=Tenant("1")
    return user