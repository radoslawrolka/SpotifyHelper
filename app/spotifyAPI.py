import base64
import json
from os import path
from requests import get, post

# Spotify API credentials ----------------------------------------------------------------------------------------------
def get_credentials(clientID, secretID):
    with open('../.credentials', 'w') as f:
        f.write(clientID + '\n')
        f.write(secretID + '\n')
    return True

def load_credentials():
    with open('../.credentials') as f:
        CLIENT_ID = f.readline().strip()
        CLIENT_SECRET = f.readline().strip()
    return CLIENT_ID, CLIENT_SECRET

# Spotify API token ----------------------------------------------------------------------------------------------------
def create_token():
    CLIENT_ID, CLIENT_SECRET = load_credentials()
    auth_str = CLIENT_ID + ':' + CLIENT_SECRET
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    with open("../.token", "w") as f:
        f.write(token)
    return token

def get_token():
    if path.getmtime("../.token") < 3600:
        with open("../.token", "r") as f:
            token = f.read()
        return token
    else:
        return create_token()

def get_auth_header():
    return {"Authorization": "Bearer " + get_token()}

# Spotify API search -----------------------------------------------------------------------------------------------
def search_artist(artist):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"q={artist}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]

def search_album(album):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"q={album}&type=album&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]

def search_song(song):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"q={song}&type=track&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]
