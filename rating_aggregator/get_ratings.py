from bs4 import BeautifulSoup
import requests
from requests import get, Session
import json
import re
import lxml
import time
import cchardet

session = Session()

# scrape imdb and metascore for movie
def get_imdb_metascore_ratings_and_synopsis(movie, year):
    try:
        response = session.get(r"https://www.imdb.com/search/title/?title="+movie+"+&title_type=feature")
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            titles = bs_object.find_all('div', class_ = "lister-item-content")
            imdb_rating = None
            metacritic_rating = None
            synopsis = None
            for title in titles:
                film_title = title.find_all('a')[0].get_text()
                film_year = title.find('span', class_ = 'lister-item-year text-muted unbold').get_text()
                if '(I' in film_year and year in film_year:
                    film_year = film_year.split(' ')
                    film_year = film_year[1]
                film_year = film_year.replace('(', '').replace(')', '')
                if film_title.lower() == movie.lower() and film_year == year:
                    if title.find('div', class_='inline-block ratings-imdb-rating'):
                        imdb_rating = (float(title.find('div', class_='inline-block ratings-imdb-rating').get('data-value'))*10)
                    if title.find('div', class_ = 'inline-block ratings-metascore'):
                        metacritic_rating = float(title.find('div', class_ = 'inline-block ratings-metascore').span.text.strip()) 
                    synopsis = title.find_all('p', class_ = "text-muted")[1].get_text()
                    break
        return film_title, film_year, imdb_rating, metacritic_rating, synopsis
    except Exception as ex:
        print(str(ex))

# scrape letterboxd rating for movie
def get_letterboxd_rating(movie, year):
    try:
        response = session.get("https://letterboxd.com/search/films/"+movie+" "+year)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            titles = bs_object.find_all('span', class_ = "film-title-wrapper")
            for title in titles:
                # Split string into substrings based on title and year
                ttl,yr = title.text.rsplit(' ', 1)
                if movie.lower() == str(ttl.lower()) and str(yr) in year: 
                    print('bloop')
                    review_endpoint = title.find('a').get('href')
                    break
        response = session.get("https://letterboxd.com"+review_endpoint)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            b = bs_object.find_all('script', type='application/ld+json')[0]
            # parse json inside script tag and use regex to return only the dict
            if json.loads( re.search(r'({.*})', b.string).group() )['aggregateRating']['ratingValue']:
                rating = round((json.loads( re.search(r'({.*})', b.string).group() )['aggregateRating']['ratingValue'] * 20), 1)
        return rating
    except Exception as ex:
        print(str(ex))

# scrape rotten tomatoes tomatometer and audience score ratings
def get_rotten_tomatoes_ratings(movie, year):
    try:
        response = session.get(r"https://www.rottentomatoes.com/search?search="+movie)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            dicts = bs_object.find_all('script', type='application/json', id='movies-json')[0]
            info = json.loads( re.search(r'({.*})', dicts.string).group() )
            tomatometer_score = None
            audience_score = None
            for item in info['items']:
                if item['name'].lower() == movie.lower() and item['releaseYear'] == year:
                    if item['tomatometerScore']['score']:
                        tomatometer_score = float(item['tomatometerScore']['score'])
                    if item['audienceScore']['score']:
                        audience_score = float(item['audienceScore']['score'])
        return tomatometer_score, audience_score
    except Exception as ex:
            print(str(ex))

# scrape tmdb rating
def get_tmdb_rating_and_movie_image(movie, year):
    tmdb_rating = None
    image_url = None
    try:
        response = session.get('https://api.themoviedb.org/3/search/movie?api_key=35847ff7af4ea4159527ddec5fa4a2f4&query='+movie+'&year='+year)
        if response.status_code == 200:
            for film in response.json()['results']:
                if film['title'].lower() == movie.lower() and year in film['release_date']:
                    if film['vote_average']:
                        tmdb_rating = (film['vote_average']*10)
                    image_base_url = 'https://image.tmdb.org/t/p/original'
                    image_endpoint = film['poster_path']
                    image_url = image_base_url + image_endpoint
                    break
        return tmdb_rating, image_url
    except Exception as ex:
            print(str(ex))    

# calculate an average rating from all ratings
def get_average_rating(imdb, metascore, letterboxd, tomatometer, audience_score, tmdb):
    all_ratings = [imdb, metascore, letterboxd, tomatometer, audience_score, tmdb]
    existing_ratings = []
    for rating in all_ratings:
        if rating is not None:
            existing_ratings.append(rating)

    avg_rating = sum(existing_ratings) / len(existing_ratings)
    avg_rating = round(avg_rating, 1)
    return avg_rating

# return all ratings
def get_all_ratings(movie, year):
    movie_title, movie_year, imdb, metascore, synopsis = get_imdb_metascore_ratings_and_synopsis(movie, year)
    tomatometer, audience_score = get_rotten_tomatoes_ratings(movie, year)
    letterboxd = get_letterboxd_rating(movie, year)
    tmdb, image = get_tmdb_rating_and_movie_image(movie, year)
    # Close session after all scraping has occurred
    session.close()
    avg = get_average_rating(imdb, metascore, tomatometer, audience_score, letterboxd, tmdb)

    return movie_title, movie_year, imdb, metascore, synopsis, tomatometer, audience_score, letterboxd, tmdb, image, avg

"""
# Testing
movie = "the dirt"
year = '2018'

title, release_year, imdb, metacritic, synopsis, tomatometer, audience, letterboxd, tmdb, image, avg = get_all_ratings(movie, year)

print("Title: " + title)
print("Year: " + release_year)
print("Synopsis: " + synopsis)
print("Movie Image: " + image)
print("Imdb: " + str(imdb))
print("Metacritic: " + str(metacritic))
print("Letterboxd: " + str(letterboxd))
print("Tomatometer: " + str(tomatometer))
print("Audience score: " + str(audience))
print("TMDB: " + str(tmdb))
print("Average: " + str(avg))
"""