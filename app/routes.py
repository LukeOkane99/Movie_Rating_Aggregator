from app import app
from flask import render_template, jsonify, request
import db

# Route for index page
@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# api endpoint to access all movies in database
@app.route('/movie_rating_aggregator/api/v1.0/ratings/all', methods=['GET'])
def get_all_ratings():
    movies = db.get_all_movies()
    return render_template('all_movies.html', title='All Movies', movies=movies)

