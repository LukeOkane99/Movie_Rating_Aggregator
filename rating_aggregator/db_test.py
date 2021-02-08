"""
from rating_aggregator import db
from rating_aggregator.models import User, Movie, WatchlistMovies

# create database if it doesn't already exist
def create_db():
    if db is None:
        db.create_all()
    else:
        print('The database already exists')

# show all records in Movies table
def get_all_movies():
    movies = Movie.query.all()
    return movies

def get_movie(ttl, yr):
    movie = Movie.query.filter_by(title=ttl, year=yr).first()
    if movie:
        return movie
    else:
        print("No record exists for this movie")

def get_all_users():
    users = User.query.all()
    return users

def get_user(email):
    user = User.query.filter_by(email=email).first()
    return user

#get_all_movies()
get_all_users()
"""