from app import app, spotifyAPI
from flask import render_template, redirect, url_for


@app.route('/')
def index():
    return render_template('index.html')

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
