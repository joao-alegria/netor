from datetime import datetime, timedelta
from flask import g, render_template, request, jsonify, make_response
from flask_oauthlib.provider import OAuth2Provider
from flask_oauthlib.contrib.oauth2 import bind_sqlalchemy
from flask_oauthlib.contrib.oauth2 import bind_cache_grant

import json
from flask import Flask
from persistance import Token, Tenant, OauthClient, Grant, session

app = Flask(__name__)
app.debug = True


def current_user():
    return g.user

def default_provider(app):
    oauth = OAuth2Provider(app)

    bind_sqlalchemy(oauth, session, user=Tenant, token=Token,
                    client=OauthClient, grant=Grant, current_user=current_user)

    app.config.update({'OAUTH2_CACHE_TYPE': 'simple'})
    bind_cache_grant(app, oauth, current_user)

    @oauth.clientgetter
    def get_client(client_id):
        return session.query(OauthClient).filter(OauthClient.client_id==client_id).first()

    @oauth.grantgetter
    def get_grant(client_id, code):
        return session.query(Grant).filter(Grant.client_id==client_id, Grant.code==code).first()

    @oauth.tokengetter
    def get_token(access_token=None, refresh_token=None):
        if access_token:
            return session.query(Token).filter(Token.access_token==access_token).first()
        if refresh_token:
            return session.query(Token).filter(Token.refresh_token==refresh_token).first()
        return None

    @oauth.grantsetter
    def set_grant(client_id, code, request, *args, **kwargs):
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            scope=' '.join(request.scopes),
            user_id=g.user.username,
            expires=expires,
        )
        session.add(grant)
        session.commit()

    @oauth.tokensetter
    def set_token(token, request, *args, **kwargs):
        # In real project, a token is unique bound to user and client.
        # Which means, you don't need to create a token every time.
        tok = Token(**token)
        tok.user_id = request.user.username
        tok.client_id = request.client.client_id
        session.add(tok)
        session.commit()

    @oauth.usergetter
    def get_user(username, password, *args, **kwargs):
        # This is optional, if you don't need password credential
        # there is no need to implement this method
        return session.query(Tenant).filter(Tenant.username == username).first()

    return oauth


def prepare_app(app):
    # client1 = OauthClient(
    #     name='dev', client_id='dev', client_secret='dev',
    #     _redirect_uris=(
    #         'http://localhost:8000/authorized '
    #         'http://localhost/authorized'
    #     ),
    # )

    client2 = OauthClient(
        name='portal', client_id='portal',
        client_secret='portal', client_type='confidential',
        _redirect_uris=(
            'http://127.0.0.1:8000/authorized '
            'http://127.0.0.1/authorized'
        ),
    )

    user = Tenant(username='admin')

    # temp_grant = Grant(
    #     user_id="admin", client_id='confidential',
    #     code='12345', scope='email',
    #     expires=datetime.utcnow() + timedelta(seconds=100)
    # )

    # access_token = Token(
    #     user_id=1, client_id='dev', access_token='expired', expires_in=0
    # )

    # access_token2 = Token(
    #     user_id=1, client_id='dev', access_token='never_expire'
    # )

    try:
        # session.add(client1)
        session.add(client2)
        session.add(user)
        # session.add(temp_grant)
        # session.add(access_token)
        # session.add(access_token2)
        session.commit()
    except:
        session.rollback()
    return app


def create_server(app, oauth=None):
    if not oauth:
        oauth = default_provider(app)

    app = prepare_app(app)

    @app.before_request
    def load_current_user():
        if "client_id" in request.args:
            clientId=request.args.get("client_id")
            client = session.query(OauthClient).filter(OauthClient.client_id==clientId).first()
            g.client = client
        if "username" in request.args:
            username=request.args.get("username")
            user = session.query(Tenant).filter(Tenant.username==username).first()
            g.user = user

    @app.route('/login')
    def home():
        return render_template('index.html')

    @app.route('/oauth/authorize', methods=['GET', 'POST'])
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
    @oauth.token_handler
    def access_token():
        return {}

    @app.route('/oauth/revoke', methods=['POST'])
    @oauth.revoke_handler
    def revoke_token():
        pass

    @app.route('/api/email')
    @oauth.require_oauth('email')
    def email_api():
        oauth = request.oauth
        return jsonify(email='me@oauth.net', username=oauth.user.username)

    @app.route('/api/client')
    @oauth.require_oauth()
    def client_api():
        oauth = request.oauth
        return jsonify(client=oauth.client.name)

    @app.route('/api/user')
    @oauth.require_oauth()
    def user_api():
        oauth = request.oauth
        return jsonify(oauth.user.getTenant()   )

    @app.route('/api/validate')
    @oauth.require_oauth()
    def validate():
        return jsonify(msg="Valid"), 200

    @oauth.invalid_response
    def require_oauth_invalid(req):
        return jsonify(message=req.error_message), 401

    return app



if __name__ == '__main__':
    app = create_server(app)
    app.run()