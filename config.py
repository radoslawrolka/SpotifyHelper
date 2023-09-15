class Config:
    with open('.credentials', 'r') as f:
        CLIENT_ID = f.readline().strip()
        CLIENT_SECRET = f.readline().strip()
    REDIRECT_URI = 'http://localhost:5000/callback'
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    SCOPE = 'user-top-read ' \
            'user-read-recently-played ' \
            'user-read-currently-playing ' \
            'user-read-playback-state ' \
            'user-modify-playback-state'
