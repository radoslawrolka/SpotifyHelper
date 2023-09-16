from app import app, spotifyAPI
from flask import render_template, request, redirect, url_for
import requests
import json

@app.route('/')
def index():
    return 'Welcome to the Spotify Top Data App! <a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    return redirect(spotifyAPI.get_auth_url())

@app.route('/callback')
def callback():
    if not spotifyAPI.validate_state():
        return 'Invalid state parameter', 400
    token = spotifyAPI.create_token()
    if token:
        return redirect(url_for('home'))
    else:
        return 'Error retrieving access token', 400

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/get_top_data')
def get_top_data():
    access_token = spotifyAPI.get_token()
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

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        type = request.form['type']
        name = request.form['name']
        return redirect(url_for('result', type=type, name=name))
    return render_template('search.html')

@app.route('/result/<type>/<name>')
def result(type, name):
    return spotifyAPI.search(type, name)
