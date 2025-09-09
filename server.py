from flask import Flask, request, jsonify, redirect, url_for
import jwt
import datetime
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.oidc.core.grants import OpenIDCode
import os


REDIRECT_URL = os.environ.get('NO_AUTH_REDIRECT_URL', 'http://localhost:3000/auth/oidc.callback')
OIDC_HOST_NAME = os.environ.get('NO_AUTH_OIDC_HOST', 'http://localhost:4000')
OIDC_USER_NAME = os.environ.get('NO_AUTH_OIDC_USER_NAME', 'admin')
OIDC_USER_MAIL = os.environ.get('NO_AUTH_OIDC_USER_MAIL', 'admin@local.net')
OIDC_CLIENT_ID = os.environ.get('NO_AUTH_OIDC_CLIENT_ID', 'client-id')
OIDC_CLIENT_SECRET = os.environ.get('NO_AUTH_OIDC_CLIENT_SECRET', 'client-secret')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

# Dummy client and user storage
clients = {
    OIDC_CLIENT_ID: {
        'client_id': OIDC_CLIENT_ID,
        'client_secret': OIDC_CLIENT_SECRET,
        'redirect_uris': [
            REDIRECT_URL,
        ],
        'response_types': ['code'],
        'grant_types': ['authorization_code'],
        'scope': 'openid profile email',
    }
}
users = {
    'user': {
        'sub': 'user', 
        'name': OIDC_USER_NAME, 
        'email': OIDC_USER_MAIL
    }
}

class DummyClient:
    def __init__(self, client_id, client_secret, redirect_uris, response_types, grant_types, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uris = redirect_uris
        self.response_types = response_types
        self.grant_types = grant_types
        self.scope = scope
    def get_client_id(self):
        return self.client_id
    def get_default_redirect_uri(self):
        return self.redirect_uris[0]
    def check_redirect_uri(self, uri):
        return uri in self.redirect_uris
    def check_client_secret(self, secret):
        return secret == self.client_secret
    def check_response_type(self, response_type):
        return response_type in self.response_types
    def check_grant_type(self, grant_type):
        return grant_type in self.grant_types
    def check_scope(self, scope):
        return True

class AuthorizationCodeGrant(OpenIDCode):
    def authenticate_user(self, authorization_code):
        return users['user']

authorization = AuthorizationServer(app)
authorization.register_grant(AuthorizationCodeGrant)

@app.route('/')
def openid_server():
    # Health check endpoint
    return jsonify({
        "status": "online"
    })

@app.route('/.well-known/openid-configuration')
@app.route('/.well-known/oidc-discovery')
def openid_config():
    # OIDC discovery endpoint
    return jsonify({
        'issuer': OIDC_HOST_NAME,
        'authorization_endpoint': f'{OIDC_HOST_NAME}/authorize',
        'token_endpoint': f'{OIDC_HOST_NAME}/token',
        'userinfo_endpoint': f'{OIDC_HOST_NAME}/userinfo',
        'jwks_uri': f'{OIDC_HOST_NAME}/jwks',
        'response_types_supported': ['code'],
        'subject_types_supported': ['public'],
        'id_token_signing_alg_values_supported': ['RS256'],
    })

@app.route('/authorize')
def authorize():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    state = request.args.get('state')
    # Check client_id and redirect_uri
    client = clients.get(client_id)
    import json
    from flask import Response
    if not client:
        error_json = json.dumps({
            'error': 'Invalid client_id',
# Uncomment the following lines for detailed debugging information
#            'client_id_received': client_id,
#            'client_id_expected': list(clients.keys()),
#            'redirect_uri_received': redirect_uri,
#            'redirect_uris_expected': [],
        }, indent=2)
        return Response(error_json, status=400, mimetype='application/json')
    if redirect_uri not in client['redirect_uris']:
        error_json = json.dumps({
            'error': 'Invalid redirect_uri',
# Uncomment the following lines for detailed debugging information
#            'client_id_received': client_id,
#            'client_id_expected': list(clients.keys()),
#            'redirect_uri_received': redirect_uri,
#            'redirect_uris_expected': client['redirect_uris'],
        }, indent=2)
        return Response(error_json, status=400, mimetype='application/json')
    code = 'dummy-code'
    return redirect(f'{redirect_uri}?code={code}&state={state}')

@app.route('/token', methods=['POST'])
def token():
    # Token endpoint with code validation
    code = request.form.get('code')
    if code != 'dummy-code':
        return jsonify({'error': 'invalid_grant', 'error_description': 'Invalid code'}), 400
    secret = app.config.get('SECRET_KEY', 'secret-key')
    now = datetime.datetime.utcnow()
    payload = {
        'iss': OIDC_HOST_NAME,
        'sub': users['user']['sub'],
        'aud': request.form.get('client_id', OIDC_CLIENT_ID),
        'exp': now + datetime.timedelta(hours=1),
        'iat': now,
        'email': users['user']['email'],
        'name': users['user']['name'],
        'preferred_username': users['user']['name'],
    }
    id_token = jwt.encode(payload, secret, algorithm='HS256')
    return jsonify({
        'access_token': 'dummy-access-token',
        'id_token': id_token,
        'token_type': 'Bearer',
        'expires_in': 3600,
    })

@app.route('/userinfo')
def userinfo():
    # Dummy userinfo endpoint
    return jsonify(users['user'])

@app.route('/jwks')
def jwks():
    # Dummy JWKS endpoint
    return jsonify({'keys': []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
