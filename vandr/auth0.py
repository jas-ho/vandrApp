import os
import requests
import json
import http.client

from flask import request, session

from vandr import app
from vandr.config import auth0_config


def auth0_query():
    # Prepare connection
    code = request.args.get('code')
    json_header = {'content-type': 'application/json'}
    token_url = 'https://{domain}/oauth/token'.format(
        domain=auth0_config['domain'])
    token_payload = {
        'client_id': auth0_config['client_id'],
        'client_secret': auth0_config['client_secret'],
        'redirect_uri': app.config['VANDR_REDIRECT'],
        'code': code,
        'grant_type': 'authorization_code'
    }
    token_info = requests.post(token_url,
                               data=json.dumps(token_payload),
                               headers=json_header).json()
    user_url = 'https://{domain}/userinfo?access_token={access_token}'.format(
        domain=auth0_config['domain'],
        access_token=token_info['access_token'])

    # request user info
    user_info_dict = requests.get(user_url).json()
    return user_info_dict


def auth0_unregister(user):
    auth0_id = user.auth0_id
    print('unregistering ' + auth0_id + '...')
    # unregister from auth0
    conn = http.client.HTTPSConnection(auth0_config['domain'])
    payload = ''
    headers = {
        'authorization': auth0_config['deletion_token'],
        'content-type': 'application/json'}
    conn.request('DELETE', '/api/v2/users/' + auth0_id, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode('utf-8'))
