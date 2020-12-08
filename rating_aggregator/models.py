from rating_aggregator import db
from datetime import datetime

# Models
class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define how User object is printed
    def __repr__(self):
        return f"User('{self.forename}', '{self.surname}', '{self.email}', '{self.admin}', '{self.date_created}')"

class Movie(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    imdb_rating = db.Column(db.Float, nullable=True)
    metascore = db.Column(db.Float, nullable=True)
    tomatometer = db.Column(db.Float, nullable=True)
    audience_score = db.Column(db.Float, nullable=True)
    letterboxd_rating = db.Column(db.Float, nullable=True)
    tmdb_rating = db.Column(db.Float, nullable=True)
    average_rating = db.Column(db.Float, nullable=False)
    movie_image = db.Column(db.String(max), nullable=False, default='default.jpg')
    synopsis = db.Column(db.Text, nullable=False, default='Unfortunately there is no synopsis available for this movie.')
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define how Movie object is printed
    def __repr__(self):
        return f"Movie('{self.title}', '{self.year}', '{self.imdb_rating}', '{self.metascore}', '{self.tomatometer}', '{self.audience_score}', '{self.letterboxd_rating}', '{self.tmdb_rating}', '{self.average_rating}', '{self.movie_image}', '{self.synopsis}', '{self.date_updated}')"

class WatchlistMovies(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), primary_key=True, nullable=False)
    movieId = db.Column(db.Integer, db.ForeignKey('movie.movieId'), primary_key=True, nullable=False)

    # Define how Movie object is printed
    def __repr__(self):
        return f"WatchlistMovies('{self.userId}', '{self.movieId}')"