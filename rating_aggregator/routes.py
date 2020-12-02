from flask import render_template, url_for, flash
from rating_aggregator import app
from rating_aggregator.models import User, Movie, WatchlistMovies

# Route for index page
@app.route('/', methods=['GET'])
@app.route('/index')
def hello():
    return "Hello Wolrd!"

# Endpoint to access all movies in the database
#@app.route('/movies/all', methods=['GET'])
#def get_all_ratings():
#    movies = db.get_all_movies()
#    return render_template('all_movies.html', title='All Movies', movies=movies)

