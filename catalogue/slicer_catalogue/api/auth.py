from flask_login import login_required, LoginManager, current_user, UserMixin
import requests
from api.settings import AuthConfig as config

loginManager = LoginManager()
current_user = current_user
login_required = login_required


class Tenant(UserMixin):
    def __init__(self, name, role):
        super().__init__()
        self.name=name
        self.role=role

    def is_admin(self):
        return self.role == 'ADMIN'


@loginManager.user_loader
def user_loader(username):
    return None


@loginManager.request_loader
def request_loader(request):
    user = None
    if "Authorization" in request.headers:
        token = request.headers.get('Authorization')
        url = f"http://{config.IDP_IP}:{config.IDP_PORT}{config.IDP_ENDPOINT}"
        response = requests.get(url, headers={"Authorization": token})

        if response.status_code==200:
            data=response.json()
            user=Tenant(data["data"]["username"], data["data"]["role"])
    return user