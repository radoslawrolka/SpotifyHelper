from flask import Flask, request, redirect, url_for, session
import requests
import base64
import json

app = Flask(__name__)

# Configure your Spotify API credentials
CLIENT_ID = 'e4731229236d48009287534c3fea2cc9'
CLIENT_SECRET = '84cba764e53c4cfd9af3020259112fe0'
REDIRECT_URI = 'http://localhost:5000/callback'  # Make sure this matches your Spotify Developer Application settings
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SCOPE = 'user-top-read user-read-recently-played user-read-currently-playing user-read-playback-state user-modify-playback-state'

app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

@app.route('/')
def index():
    return 'Welcome to the Spotify Top Data App! <a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    # Generate a random state value to prevent cross-site request forgery (CSRF) attacks
    state = 'some_random_state_value'

    # Create the authorization URL with required parameters
    auth_url = f'{AUTH_URL}?response_type=code' \
               f'&client_id={CLIENT_ID}' \
               f'&redirect_uri={REDIRECT_URI}' \
               f'&scope={SCOPE}' \
               f'&state={state}'

    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Check the state parameter to protect against CSRF attacks
    if request.args.get('state') != 'some_random_state_value':
        return 'Invalid state parameter', 400

    # Exchange the authorization code for an access token
    code = request.args.get('code')
    token_data = {
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode(),
    }
    response = requests.post(TOKEN_URL, data=token_data, headers=headers)

    if response.status_code == 200:
        token_info = json.loads(response.text)
        session['access_token'] = token_info['access_token']
        return redirect(url_for('home'))
    else:
        return 'Error retrieving access token', 400

@app.route('/home')
def home():
    return 'Welcome to the Spotify Top Data App!</br> ' \
           '<a href="/get_top_data">get top user data</a></br>' \
           '<a href="/current_play">get current play</a></br>'

@app.route('/get_top_data')
def get_top_data():
    access_token = session.get('access_token')
    if not access_token:
        return 'Access token not found in session'

    # Make a request to the Spotify API to get the user's top data
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)

    if response.status_code == 200:
        top_artists_data = json.loads(response.text)
        # Process and display the user's top artists data here
        return top_artists_data
    else:
        return 'Error fetching top artists data', 400

@app.route('/current_play')
def current_play():
    access_token = session.get('access_token')
    if not access_token:
        return 'Access token not found in session'

    # Make a request to the Spotify API to get the user's top data
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    if response.status_code == 200:
        current = json.loads(response.text)
        # Process and display the user's top artists data here
        return current['item']['name'] + ' by ' + current['item']['artists'][0]['name'] + ' from ' + current['item']['album']['name']
    else:
        return response.text+'Error fetching current song playing', 400

if __name__ == '__main__':
    app.run(debug=False)
