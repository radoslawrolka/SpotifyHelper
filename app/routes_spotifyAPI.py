from app import app, spotifyAPI
from flask import render_template, request, redirect, jsonify


@app.route('/your-top-artists')
def get_top_artists():
    user_top_data = spotifyAPI.get_top_data("artists")
    return render_template('your-top.html', data=user_top_data, item="artists")


@app.route('/your-top-tracks')
def get_top_tracks():
    user_top_data = spotifyAPI.get_top_data("tracks")
    return render_template('your-top.html', data=user_top_data, item="tracks")


@app.route('/<item>/<name>')
def show_item(item, name):
    result_data = spotifyAPI.search(item, name, 1)
    return render_template('show.html', result=result_data, item=item, name=name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_item = request.form['item']
        search_name = request.form['name']
        return redirect(f'/search/result/{search_item}/{search_name}')
    return render_template('search.html')


@app.route('/search/result/<item>/<name>', methods=['GET'])
def search_result(item, name):
    result_data = spotifyAPI.search(item, name)
    return render_template(f'search-result.html', result=result_data, item=item, name=name)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        genres = ",".join(request.json.get('selected_genres'))
        artist_name = request.json.get('artist_name', '')
        track_name = request.json.get('track_name', '')
        if artist_name == '':
            artist_name = '0'
        if track_name == '':
            track_name = '0'
        return jsonify(genre=genres, artist=artist_name, track=track_name)
    else:
        genres = spotifyAPI.get_genre_seeds()
        return render_template('recommend.html', genres=genres)


@app.route('/recommend/result/<genres>/<artist>/<track>', methods=['GET', 'POST'])
def recommend_result(genres, artist, track):
    track_id = None
    artist_id = None
    if artist != "0":
        artist_id = spotifyAPI.search("artist", artist, 1)[0]['id']
    if track != "0":
        track_id = spotifyAPI.search("track", track, 1)[0]['id']
    result = spotifyAPI.get_recommendations(genres, artist_id, track_id)
    gen = spotifyAPI.get_genre_seeds()
    return render_template('recommend-result.html',
                           genres=gen,
                           result=result,
                           genres_selected=genres.split(','),
                           artist_selected=artist,
                           track_selected=track)

@app.route('/your-recommend', methods=['GET', 'POST'])
def your_recommend():
    your_artist = spotifyAPI.get_top_data("artists")
    artists = ",".join([artist['id'] for artist in your_artist[:3]])
    your_track = spotifyAPI.get_top_data("tracks")
    tracks = ",".join([track['id'] for track in your_track[:3]])
    result = spotifyAPI.get_recommendations(None, artists, tracks)
    return render_template('your-recommend.html', data=result, artists=artists, tracks=tracks)
