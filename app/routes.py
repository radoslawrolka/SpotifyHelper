from app import app
from flask import render_template, request, redirect, url_for, session
import requests
import base64
import json
from app import spotifyCharts

@app.route('/')
def index():
    return 'Welcome to the Spotify Top Data App! <a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    # Generate a random state value to prevent cross-site request forgery (CSRF) attacks
    state = 'some_random_state_value'

    # Create the authorization URL with required parameters
    auth_url = f'{app.config["AUTH_URL"]}?response_type=code' \
               f'&client_id={app.config["CLIENT_ID"]}' \
               f'&redirect_uri={app.config["REDIRECT_URI"]}' \
               f'&scope={app.config["SCOPE"]}' \
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
        'redirect_uri': app.config["REDIRECT_URI"],
        'grant_type': 'authorization_code',
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{app.config["CLIENT_ID"]}:{app.config["CLIENT_SECRET"]}'.encode()).decode(),
    }
    response = requests.post(app.config["TOKEN_URL"], data=token_data, headers=headers)

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
           '<a href="/current_play">get current play</a></br>' \
           '<a href="/most-streamed-songs">most streamed songs</a>'

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
# ranking --------------------------------------------------------------------------------------------------------------
@app.route('/most-streamed-songs')
def ranking():
    data = spotifyCharts.get_top_songs()
    return render_template('most-streamed-songs.html', data=data)


