from app import app
from flask import request
import base64
import json
import requests
import random
import os

# utility functions ----------------------------------------------------------------------------------------------------
def get_random_string(length):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    result_str = ''.join(random.choice(chars) for _ in range(length))
    return result_str

# Spotify API token ----------------------------------------------------------------------------------------------------
def get_auth_url():
    app.config['state'] = get_random_string(16)
    auth_url = f'{app.config["AUTH_URL"]}?response_type=code' \
               f'&client_id={app.config["CLIENT_ID"]}' \
               f'&redirect_uri={app.config["REDIRECT_URI"]}' \
               f'&scope={app.config["SCOPE"]}' \
               f'&state={app.config.get("state")}'
    return auth_url

def validate_state():
    return request.args.get('state') == app.config.get('state')

def create_token():
    code = request.args.get('code')
    token_data = {
        'code': code,
        'redirect_uri': app.config["REDIRECT_URI"],
        'grant_type': 'authorization_code',
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(
            f'{app.config["CLIENT_ID"]}:{app.config["CLIENT_SECRET"]}'.encode()).decode(),
    }
    response = requests.post(app.config["TOKEN_URL"], data=token_data, headers=headers)

    if response.status_code == 200:
        token = json.loads(response.text)['access_token']
        refresh = json.loads(response.text)['refresh_token']
        with open(".token", "w") as f:
            f.write(token)
            f.write("\n")
            f.write(refresh)
        return token
    else:
        return None

def refresh_token():
    with open(".token", "r") as f:
        refresh = f.readlines()[1]
    token_data = {
        'refresh_token': refresh,
        'grant_type': 'refresh_token',
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(
            f'{app.config["CLIENT_ID"]}:{app.config["CLIENT_SECRET"]}'.encode()).decode(),
    }
    response = requests.post(app.config["TOKEN_URL"], data=token_data, headers=headers)

    if response.status_code == 200:
        token = json.loads(response.text)['access_token']
        with open(".token", "w") as f:
            f.write(token)
            f.write("\n")
            f.write(refresh)
        return token
    else:
        return None

def get_token():
    if os.path.getmtime(".token") < 3599:
        with open(".token", "r") as f:
            token = f.read()
        return token
    else:
        return refresh_token()

def get_auth_header():
    return {"Authorization": "Bearer " + get_token()}

# Spotify API search -----------------------------------------------------------------------------------------------
def search(type, name): # type = [artist/album/track]
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"q={name}&type={type}&limit=1"

    query_url = url + "?" + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)[type+"s"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]
