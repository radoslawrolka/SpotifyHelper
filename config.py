class Config:
    # Configure your Spotify API credentials
    CLIENT_ID = '<your_client_id>'
    CLIENT_SECRET = '<your_client_secret>'
    REDIRECT_URI = 'http://localhost:5000/callback'
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    SCOPE = 'user-top-read user-read-recently-played user-read-currently-playing user-read-playback-state user-modify-playback-state'