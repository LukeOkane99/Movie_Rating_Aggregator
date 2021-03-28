import pytest
from rating_aggregator import create_app, db, bcrypt
from rating_aggregator.test_config import test_Config
from rating_aggregator.models import User, Movie, WatchlistMovies

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=test_Config)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # create an application context
        with flask_app.app_context():
            yield testing_client  # this is where testing occurs

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create database and tables
    db.create_all()

    # Hash test passwords
    password1 = bcrypt.generate_password_hash('reallysecurepassword').decode('utf-8')
    password2 = bcrypt.generate_password_hash('PaSsWoRd').decode('utf-8') 

    # Insert test users
    user1 = User(forename='Test', surname='User', email='test-user36@gmail.com', password=password1, admin=True)
    user2 = User(forename='Scott', surname='Williams', email='swilliams-99@gmail.com', password=password2)

    # Insert test movie
    movie1 = Movie(title='Gladiator', year='2000', imdb_rating=85.0, imdb_votes=1353601, imdb_url='https://www.imdb.com/title/tt0172495/', metascore=67.0, metascore_votes=46, metacritic_url='https://www.metacritic.com/movie/gladiator', tomatometer=77.0, tomatometer_votes=200, audience_score=87.0, audience_score_votes=34128168, rotten_tomatoes_url='https://rottentomatoes.com/m/gladiator', letterboxd_rating=79.0,
     letterboxd_votes=205814, letterboxd_url='https://letterboxd.com/film/gladiator-2000/', tmdb_rating=82.0, tmdb_votes=13372, tmdb_url='https://www.themoviedb.org/movie/98', average_rating=86.9, movie_image='https://image.tmdb.org/t/p/original/ehGpN04mLJIrSnxcZBMvHeG0eDc.jpg', synopsis='A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.')

    # Insert entry into user1 watchlist
    #entry = WatchlistMovies(userId=1, movieId=1)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(movie1)
    #db.session.add(entry)

    # Commit changes to User table
    db.session.commit()

    yield  # this is where the testing occurs

    db.drop_all()

@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='anna-taylor36@gmail.com', password='reallysecurepassword'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
