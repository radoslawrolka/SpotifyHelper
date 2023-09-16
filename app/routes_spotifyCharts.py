from app import app, spotifyCharts
from flask import render_template

@app.route('/most-streamed-songs')
def most_streamed_songs():
    data = spotifyCharts.get_top_songs()
    return render_template('most-streamed-songs.html', data=data)

@app.route('/most-streamed-artists')
def most_streamed_artists():
    data = spotifyCharts.get_top_artists()
    return render_template('most-streamed-artists.html', data=data)

@app.route('/most-streamed-albums')
def most_streamed_albums():
    data = spotifyCharts.get_top_albums()
    return render_template('most-streamed-albums.html', data=data)
