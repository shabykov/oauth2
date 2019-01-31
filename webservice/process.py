import flask
import logging
import requests


HTTP_OK = 200
HTTP_FORBIDDEN = 403
HTTP_BAD_REQUEST = 404

OAUTH2_SERVER = 'http://127.0.0.1:8000'
CLIENT_ID = 'i1I8uiN1vdpVoenFi4t7zXqVylYupZbN1gEQh2Vn'
CLIENT_SECRET = 'NqEb8RWzMmEtR7Ynq36SOVHqF94Ib2sLJBBiN5Vsd9FPeA2LBgVsqIKtG3S42t4ydNiCmLjNXAqMETb2enlzFoNArwbHU5ussq19yrt13tjIhOchQAUUbthZGPSPlBbB'
REDIRECT_URI = 'http://127.0.0.1:8081/oauth2callback'


API_VERSION = 'v1'

app = flask.Flask(__name__, template_folder='templates')

app.secret_key = "qwerty12345"


def create_access_token(code):
    body = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    try:
        resp = requests.post(
            url=OAUTH2_SERVER + '/o/token/',
            data=body
        )
        if resp.status_code == HTTP_OK:
            return HTTP_OK, resp.json()
        elif resp.status_code == HTTP_FORBIDDEN:
            return HTTP_FORBIDDEN, resp.json()
    except Exception as error:
        logging.error(error)
    return HTTP_BAD_REQUEST, {'message': 'internal error'}


def get_authorized_user(access_token):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    try:
        resp = requests.get(
            url=OAUTH2_SERVER + '/api/{}/authorized-user-info/'.format(API_VERSION),
            headers=headers
        )
        if resp.status_code == HTTP_OK:
            return HTTP_OK, resp.json()
        elif resp.status_code == HTTP_FORBIDDEN:
            return HTTP_FORBIDDEN, resp.json()

    except Exception as error:
        logging.error(error)
    return HTTP_BAD_REQUEST, {'error': 'internal error'}


def get_access_token_info(access_token):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    try:
        resp = requests.get(
            url=OAUTH2_SERVER + '/api/{}/token-info/'.format(API_VERSION),
            headers=headers
        )
        if resp.status_code == HTTP_OK:
            return HTTP_OK, resp.json()
        elif resp.status_code == HTTP_FORBIDDEN:
            return HTTP_FORBIDDEN, resp.json()

    except Exception as error:
        logging.error(error)
    return HTTP_BAD_REQUEST, {'error': 'internal error'}


@app.route('/oauth2callback/')
def oauth2callback():

    code = flask.request.args.get("code", None)
    if code:
        status, body = create_access_token(code)
        if status == HTTP_OK:
            # status, user = get_authorized_user(body['access_token'])
            status, body = get_access_token_info(body['access_token'])

    else:
        body = {'error': flask.request.args.get("error", None)}
        status = HTTP_FORBIDDEN

    response = flask.jsonify(body)
    response.status_code = status
    return response


@app.route('/index/', methods=['GET'])
def index():
    return flask.render_template('index.html'), 200


if __name__ == '__main__':
    app.run(port=8081, debug=True)
