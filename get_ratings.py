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
def get_imdb_metascore_ratings(movie, year):
    try:
        response = session.get(r"https://www.imdb.com/search/title/?title="+movie+"+&title_type=feature")
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            titles = bs_object.find_all('div', class_ = "lister-item-content")
            for title in titles:
                film_title = title.find_all('a')[0].get_text()
                film_year = title.find('span', class_ = 'lister-item-year text-muted unbold').get_text()
                film_year = film_year.replace('(', '').replace(')', '')
                if film_title.lower() == movie.lower() and film_year == year:
                    imdb_rating = title.find('div', class_='inline-block ratings-imdb-rating').get('data-value')
                    metacritic_rating = title.find('div', class_ = 'inline-block ratings-metascore').span.text.strip()
                    break
    except Exception as ex:
        print(str(ex))
    finally:
        return film_title, film_year, ((float(imdb_rating))*10), float(metacritic_rating)

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
                if movie.lower() == ttl.lower() and yr in year:  
                    review_endpoint = title.find('a').get('href')
                    break
    except Exception as ex:
        print(str(ex))
    finally:
        try:
            response = session.get("https://letterboxd.com"+review_endpoint)
            if response.status_code == 200:
                bs_object = BeautifulSoup(response.content, 'lxml')
                b = bs_object.find_all('script', type='application/ld+json')[0]
                # parse json inside script tag and use regex to return only the dict
                rating = json.loads( re.search(r'({.*})', b.string).group() )['aggregateRating']['ratingValue']
        except Exception as ex:
            print(str(ex))
        finally:
            return round((rating*20), 1)

# scrape rotten tomatoes tomatometer and audience score ratings
def get_rotten_tomatoes_ratings(movie, year):
    try:
        response = session.get(r"https://www.rottentomatoes.com/search?search="+movie)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            dicts = bs_object.find_all('script', type='application/json', id='movies-json')[0]
            info = json.loads( re.search(r'({.*})', dicts.string).group() )
            for item in info['items']:
                if item['name'].lower() == movie.lower() and item['releaseYear'] == year:
                    tomatometer_score = item['tomatometerScore']['score']
                    audience_score = item['audienceScore']['score']
                    break
    except Exception as ex:
            print(str(ex))
    finally:
        return float(tomatometer_score), float(audience_score)

# scrape tmdb rating
def get_tmdb_rating(movie, year):
    try:
        response = session.get('https://api.themoviedb.org/3/search/movie?api_key=35847ff7af4ea4159527ddec5fa4a2f4&query='+movie+'&year='+year)
        if response.status_code == 200:
            for film in response.json()['results']:
                if film['title'].lower() == movie.lower() and year in film['release_date']:
                    tmdb_rating = film['vote_average']
                    break
    except Exception as ex:
            print(str(ex))    
    finally:
        return (tmdb_rating*10)

# calculate an average rating from all ratings
def get_average_rating(imdb, metascore, letterboxd, tomatometer, audience_score, tmdb):
    avg_rating = (imdb+metascore+letterboxd+tomatometer+audience_score+tmdb) / 6
    avg_rating = round(avg_rating, 1)
    return avg_rating

# return all ratings
def get_all_ratings(movie, year):
    title, year, imdb, metascore = get_imdb_metascore_ratings(movie, year)
    tomatometer, audience_score = get_rotten_tomatoes_ratings(movie, year)
    letterboxd = get_letterboxd_rating(movie, year)
    tmdb = get_tmdb_rating(movie, year)
    # Close session after all scraping has occurred
    session.close()
    avg = get_average_rating(imdb, metascore, tomatometer, audience_score, letterboxd, tmdb)

    return title, year, imdb, metascore, tomatometer, audience_score, letterboxd, tmdb, avg
