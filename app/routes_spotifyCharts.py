from app import app, spotifyCharts
from flask import render_template

@app.route('/most-streamed-tracks')
def most_streamed_songs():
    data = spotifyCharts.get_top_songs()
    return render_template('most-streamed.html', data=data, item="tracks")

@app.route('/most-streamed-artists')
def most_streamed_artists():
    data = spotifyCharts.get_top_artists()
    return render_template('most-streamed.html', data=data, item="artists")

@app.route('/most-streamed-albums')
def most_streamed_albums():
    data = spotifyCharts.get_top_albums()
    return render_template('most-streamed.html', data=data, item="albums")
