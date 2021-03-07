from rating_aggregator import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime, date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Models
class User(db.Model, UserMixin):
    # Convert datetime to dd/mm/yyyy 
    current_date = datetime.utcnow().strftime('%d/%m/%Y')

    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=0)
    date_created = db.Column(db.String(10), nullable=False, default=current_date)

    # Create token
    def get_reset_token(self, expires=1800):
        s = Serializer(app.config['SECRET_KEY'], expires)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # Verify token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    # Define how User object is printed
    def __repr__(self):
        return f"User('{self.id}', '{self.forename}', '{self.surname}', '{self.email}', '{self.admin}', '{self.date_created}')"

class Movie(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    imdb_rating = db.Column(db.Float, nullable=True)
    imdb_votes = db.Column(db.Integer, nullable=True)
    imdb_url = db.Column(db.Text, nullable=True)
    metascore = db.Column(db.Float, nullable=True)
    metascore_votes = db.Column(db.Integer, nullable=True)
    metacritic_url = db.Column(db.Text, nullable=True)
    tomatometer = db.Column(db.Float, nullable=True)
    tomatometer_votes = db.Column(db.Integer, nullable=True)
    audience_score = db.Column(db.Float, nullable=True)
    audience_score_votes = db.Column(db.Integer, nullable=True)
    rotten_tomatoes_url = db.Column(db.Text, nullable=True)
    letterboxd_rating = db.Column(db.Float, nullable=True)
    letterboxd_votes = db.Column(db.Integer, nullable=True)
    letterboxd_url = db.Column(db.Text, nullable=True)
    tmdb_rating = db.Column(db.Float, nullable=True)
    tmdb_votes = db.Column(db.Integer, nullable=True)
    tmdb_url = db.Column(db.Text, nullable=True)
    average_rating = db.Column(db.Float, nullable=False)
    movie_image = db.Column(db.Text, nullable=False, default='https://bigears.info/wp-content/themes/bigears/images/image-not-found.jpg')
    synopsis = db.Column(db.Text, nullable=False, default='Unfortunately there is no synopsis available for this movie.')
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # Define how Movie object is printed
    def __repr__(self):
        return f"Movie('{self.title}', '{self.year}', '{self.imdb_rating}', '{self.imdb_votes}', '{self.imdb_url}', '{self.metascore}', '{self.metascore_votes}', '{self.metacritic_url}', '{self.tomatometer}', '{self.tomatometer_votes}', '{self.audience_score}', '{self.audience_score_votes}', '{self.rotten_tomatoes_url}', '{self.letterboxd_rating}', '{self.letterboxd_votes}', '{self.letterboxd_url}', '{self.tmdb_rating}', '{self.tmdb_votes}', '{self.tmdb_url}', '{self.average_rating}', '{self.movie_image}', '{self.synopsis}', '{self.date_updated}')"

class WatchlistMovies(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    movieId = db.Column(db.Integer, db.ForeignKey('movie.movieId'), primary_key=True, nullable=False)

    # Define how Movie object is printed
    def __repr__(self):
        return f"WatchlistMovies('{self.userId}', '{self.movieId}')"