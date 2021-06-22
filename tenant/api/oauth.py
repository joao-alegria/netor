from flask_oauthlib.provider import OAuth2Provider
from db.persistance import OauthToken, Tenant, OauthClient, OauthGrant, DB
from datetime import datetime, timedelta
from flask import g

def currentUser():
    return g.user

def OauthProvider(app):
    oauth = OAuth2Provider(app)

    @oauth.clientgetter
    def get_client(client_id):
        return DB.session.query(OauthClient).filter(OauthClient.client_id==client_id).first()

    @oauth.grantgetter
    def get_grant(client_id, code):
        return DB.session.query(OauthGrant).filter(OauthGrant.client_id==client_id, OauthGrant.code==code).first()

    @oauth.tokengetter
    def get_token(access_token=None, refresh_token=None):
        if access_token:
            return DB.session.query(OauthToken).filter(OauthToken.access_token==access_token).first()
        if refresh_token:
            return DB.session.query(OauthToken).filter(OauthToken.refresh_token==refresh_token).first()
        return None

    @oauth.grantsetter
    def set_grant(client_id, code, request, *args, **kwargs):
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = OauthGrant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            scope=' '.join(request.scopes),
            user_id=g.user.username,
            expires=expires,
        )
        DB.session.add(grant)
        DB.session.commit()

    @oauth.tokensetter
    def set_token(token, request, *args, **kwargs):
        tok = DB.session.query(OauthToken).filter(OauthToken.client_id==request.client.client_id, OauthToken.user_id==request.user.username).first()

        # make sure that every client has only one token connected to a user
        expires_in = token.get('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)
        if tok==None:
            tok = OauthToken(
                access_token=token['access_token'],
                refresh_token=token['refresh_token'],
                token_type=token['token_type'],
                _scopes=token['scope'],
                expires=expires,
                client_id=request.client.client_id,
                user_id=request.user.username,
            )
        else:
            tok.access_token=token['access_token']
            tok.refresh_token=token['refresh_token']
            tok.token_type=token['token_type']
            tok._scopes=token['scope']
            tok.expires=expires
            tok.client_id=request.client.client_id
            tok.user_id=request.user.username

        DB.session.add(tok)
        DB.session.commit()

        return tok

    @oauth.usergetter
    def get_user(username, password, *args, **kwargs):
        user=DB.session.query(Tenant).filter(Tenant.username == username).first()
        if user.check_password(password):
            return user
        return None

    return oauth
