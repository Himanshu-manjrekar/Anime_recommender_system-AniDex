import requests
import os

from flask import Flask, render_template, request, redirect, url_for
from src.pipeline.predict_pipeline import Prediction


app = Flask(__name__)

# Jikan API base URL
JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

@app.route('/')
def home():
    # Get top anime from Jikan API
    top_response = requests.get(f"{JIKAN_API_BASE_URL}/top/anime", params={"limit": 12})
    top_anime = []
    if top_response.status_code == 200:
        top_anime = top_response.json().get('data', [])
    
    # Get seasonal anime from Jikan API
    seasonal_response = requests.get(f"{JIKAN_API_BASE_URL}/seasons/now", params={"limit": 12})
    seasonal_anime = []
    if seasonal_response.status_code == 200:
        seasonal_anime = seasonal_response.json().get('data', [])
    
    return render_template('index.html', 
                           top_anime=top_anime, 
                           seasonal_anime=seasonal_anime,
                           search_results=None)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('home'))
    prediction = Prediction()
    search_results = prediction.perform_prediction(query)
    return render_template('search.html', search_results=search_results, num_anime = 10)

@app.route('/top')
def top():
    # Get top anime from Jikan API (more results for dedicated page)
    response = requests.get(f"{JIKAN_API_BASE_URL}/top/anime", params={"limit": 24})
    top_anime = []
    if response.status_code == 200:
        top_anime = response.json().get('data', [])
    
    return render_template('top.html', top_anime=top_anime)

@app.route('/seasonal')
def seasonal():
    # Get seasonal anime from Jikan API (more results for dedicated page)
    response = requests.get(f"{JIKAN_API_BASE_URL}/seasons/now", params={"limit": 24})
    seasonal_anime = []
    if response.status_code == 200:
        seasonal_anime = response.json().get('data', [])
    
    return render_template('seasonal.html', seasonal_anime=seasonal_anime)

@app.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    # Get anime details from Jikan API
    response = requests.get(f"{JIKAN_API_BASE_URL}/anime/{anime_id}")
    anime = None
    if response.status_code == 200:
        anime = response.json().get('data')
    
    if not anime:
        return render_template('error.html', message="Anime not found"), 404
    
    # Format genres and studios for display
    genres = ", ".join([genre['name'] for genre in anime.get('genres', [])])
    studios = ", ".join([studio['name'] for studio in anime.get('studios', [])])
    
    return render_template('anime_detail.html', anime=anime, genres=genres, studios=studios)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', message="Internal server error"), 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)s