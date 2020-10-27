from app import app
from flask import render_template, jsonify, request

movies = [
        {
            'name' : 'the dark knight',
            'year': '2008',
            'rating' : '90'
        },
        {
            'name' : 'the dark knight rises',
            'year' : '2012',
            'rating': '79'
        }

    ]

# Route for index page
@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# api endpoint to access all movies in database
@app.route('/movie_rating_aggregator/api/v1.0/ratings/all', methods=['GET'])
def get_all_ratings():
    return jsonify(movies)
