from app import app, spotifyAPI
from flask import render_template, request, redirect


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


"""
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        input_text = request.args.get('input')
        #data = request.form['data']
        print(input_text)
        return
        return redirect(f'/recommend/result/{data}')
    return render_template('recommend.html')


@app.route('/recommend/result/<data>', methods=['GET'])
def recommendations(data):
    result_data = spotifyAPI.get_recommendations(data)
    return render_template('recommend-result.html', result=result_data, data=data)

"""