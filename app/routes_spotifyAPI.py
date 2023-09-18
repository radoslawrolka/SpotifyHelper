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
        selected = ",".join(request.json.get('selected_genres'))
        return jsonify(selected)
    else:
        genres = spotifyAPI.get_genre_seeds()
        return render_template('recommend.html', genres=genres)


@app.route('/recommend/result/<genres>', methods=['GET', 'POST'])
def recommend_result(genres):
    result = spotifyAPI.get_recommendations(genres)
    gen = spotifyAPI.get_genre_seeds()
    return render_template('recommend-result.html', genres=gen, result=result)
