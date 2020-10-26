from app import app
from flask import render_template

# Route for index page
@app.route('/')
@app.route('/index')
def index():
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
    return render_template('index.html', title='Home', movies=movies)
