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
    imdb_rating = None
    metacritic_rating = None
    synopsis = None
    imdb_votes = None
    metacritic_votes = None
    imdb_url = None
    metacritic_url = None
    try:
        response = session.get(r"https://www.imdb.com/search/title/?title="+movie+"+&title_type=feature")
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            titles = bs_object.find_all('div', class_ = "lister-item-content")
            for title in titles:
                movie_title = title.find_all('a')[0].get_text()
                movie_year = title.find('span', class_ = 'lister-item-year text-muted unbold').get_text()
                if '(I' in movie_year and year in movie_year:
                    movie_year = movie_year.split(' ')
                    movie_year = movie_year[1]
                movie_year = movie_year.replace('(', '').replace(')', '')
                if movie_title.lower() == movie.lower() and movie_year == year:
                    film_title = movie_title
                    film_year = movie_year
                    imdb_url = 'https://www.imdb.com'+str(title.find_all('a')[0].get('href'))
                    if title.find('div', class_='inline-block ratings-imdb-rating'):
                        imdb_rating = (float(title.find('div', class_='inline-block ratings-imdb-rating').get('data-value'))*10)
                        spans = title.find('p', class_='sort-num_votes-visible').find_all('span')
                        imdb_votes = int(spans[1].get('data-value'))
                    if title.find('div', class_ = 'inline-block ratings-metascore'):
                        metacritic_rating = float(title.find('div', class_ = 'inline-block ratings-metascore').span.text.strip()) 
                    synopsis = title.find_all('p', class_ = "text-muted")[1].get_text()
                    break
        # getting metacritic total number of voters
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        }
        response = session.get("https://www.metacritic.com/search/movie/"+movie+"/results", headers=headers)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            titles = bs_object.find_all('div', class_ = "main_stats")
            for title in titles:
                movie_title = title.find('a').get_text().strip()
                movie_year = title.find('p').get_text().strip().split(' ')
                movie_year = movie_year[1]
                if movie_title.lower() == movie.lower() and movie_year == year:
                    endpoint = title.find('a').get('href')
                    response = session.get('https://www.metacritic.com'+endpoint, headers=headers)
                    metacritic_url = 'https://www.metacritic.com'+endpoint
                    bs_object = BeautifulSoup(response.content, 'lxml')
                    info = bs_object.find('script', type='application/ld+json')
                    if json.loads(info.string)['aggregateRating']['ratingValue']:
                        metacritic_votes = int(json.loads(info.string)['aggregateRating']['ratingCount'])
                        break
        return film_title, film_year, imdb_rating, imdb_votes, metacritic_rating, metacritic_votes, synopsis, imdb_url, metacritic_url
    except Exception as ex:
        print(str(ex))

# scrape letterboxd rating for movie
def get_letterboxd_rating(movie, year):
    rating = None
    letterboxd_votes = None
    review_endpoint = None
    letterboxd_url = None
    try:
        response = session.get("https://letterboxd.com/search/films/"+movie+" "+year)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            titles = bs_object.find_all('span', class_ = "film-title-wrapper")
            for title in titles:
                # Split string into substrings based on title and year
                ttl,yr = title.text.rsplit(' ', 1)
                if movie.lower() == str(ttl.lower()) and str(yr) in year: 
                    review_endpoint = title.find('a').get('href')
                    break
        if review_endpoint is not None:
            response = session.get("https://letterboxd.com"+review_endpoint)
            if response.status_code == 200:
                letterboxd_url = "https://letterboxd.com"+review_endpoint
                bs_object = BeautifulSoup(response.content, 'lxml')
                info = bs_object.find_all('script', type='application/ld+json')[0]
                # parse json inside script tag and use regex to return only the dict
                if json.loads( re.search(r'({.*})', info.string).group() )['aggregateRating']['ratingValue']:
                    rating = round((json.loads( re.search(r'({.*})', info.string).group() )['aggregateRating']['ratingValue'] * 20), 1)
                    letterboxd_votes = int(json.loads( re.search(r'({.*})', info.string).group() )['aggregateRating']['ratingCount'])
        return rating, letterboxd_votes, letterboxd_url
    except Exception as ex:
        print(str(ex))

# scrape rotten tomatoes tomatometer and audience score ratings
def get_rotten_tomatoes_ratings(movie, year):
    tomatometer_score = None
    tomatometer_votes = None
    audience_score = None
    audience_score_votes = None
    rotten_tomatoes_url = None
    try:
        response = session.get(r"https://www.rottentomatoes.com/search?search="+movie)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            dicts = bs_object.find_all('script', type='application/json', id='movies-json')[0]
            info = json.loads( re.search(r'({.*})', dicts.string).group() )
            for item in info['items']:
                if item['name'].lower() == movie.lower() and item['releaseYear'] == year:
                    rotten_tomatoes_url = item['url']
                    response = session.get(rotten_tomatoes_url)
                    if response.status_code == 200:
                        bs_object = BeautifulSoup(response.content, 'lxml')
                        script = bs_object.find_all('script', type='application/json')[0]
                        info = json.loads( re.search(r'({.*})', script.string).group() )
                        if info['scoreboard']['tomatometerScore']:
                            tomatometer_score = float(info['scoreboard']['tomatometerScore'])
                            tomatometer_votes = int(info['scoreboard']['tomatometerCount'])
                        if info['scoreboard']['audienceScore']:
                            audience_score = float(info['scoreboard']['audienceScore'])
                            audience_score_votes = int(info['scoreboard']['audienceCount'])
        return tomatometer_score, tomatometer_votes, audience_score, audience_score_votes, rotten_tomatoes_url
    except Exception as ex:
            print(str(ex))

# scrape tmdb rating
def get_tmdb_rating_and_movie_image(movie, year):
    tmdb_rating = None
    tmdb_votes = None
    image_url = None
    tmdb_url = None
    try:
        response = session.get('https://api.themoviedb.org/3/search/movie?api_key=35847ff7af4ea4159527ddec5fa4a2f4&query='+movie+'&year='+year)
        if response.status_code == 200:
            for film in response.json()['results']:
                if film['title'].lower() == movie.lower() and year in film['release_date']:
                    if film['vote_average']:
                        tmdb_rating = (film['vote_average']*10)
                        tmdb_votes = int(film['vote_count'])
                    image_base_url = 'https://image.tmdb.org/t/p/original'
                    image_endpoint = film['poster_path']
                    image_url = image_base_url + image_endpoint
                    movie_id = film['id']
                    tmdb_url = 'https://www.themoviedb.org/movie/'+str(movie_id)
                    break
        return tmdb_rating, tmdb_votes, image_url, tmdb_url
    except Exception as ex:
            print(str(ex))    

# calculate an average rating from all ratings
def get_average_rating(imdb, imdb_votes, metascore, meta_votes, letterboxd, ltrboxd_votes, tomatometer, tmtomtr_votes, audience_score, aud_scr_votes, tmdb, tmdb_votes):
    all_votes = [imdb_votes, meta_votes, ltrboxd_votes, tmtomtr_votes, aud_scr_votes, tmdb_votes]
    existing_votes = []
    for votes in all_votes:
        if votes is not None:
            existing_votes.append(votes)
            total_votes = sum(existing_votes)

    weighted_scores = []

    if imdb is not None and imdb_votes is not None:
        imdb_weighted = (imdb*imdb_votes)
        weighted_scores.append(imdb_weighted)
    if metascore is not None and meta_votes is not None:
        meta_weighted = (metascore*meta_votes)
        weighted_scores.append(meta_weighted)
    if letterboxd is not None and ltrboxd_votes is not None:
        letterboxd_weighted = (letterboxd*ltrboxd_votes)
        weighted_scores.append(letterboxd_weighted)
    if tomatometer is not None and tmtomtr_votes is not None:
        tomatometer_weighted = (tomatometer*tmtomtr_votes)
        weighted_scores.append(tomatometer_weighted)
    if audience_score is not None and aud_scr_votes is not None:
        audience_score_weighted = (audience_score*aud_scr_votes)
        weighted_scores.append(audience_score_weighted)
    if tmdb is not None and tmdb_votes is not None:
        tmdb_weighted = (tmdb*tmdb_votes)
        weighted_scores.append(tmdb_weighted)

    product_of_rating_and_votes = sum(weighted_scores)

    avg_rating = product_of_rating_and_votes / total_votes

    avg_rating = round(avg_rating, 1)
    return avg_rating

# return all ratings
def get_all_ratings(movie, year):
    movie_title, movie_year, imdb, imdb_votes, metascore, metascore_votes, synopsis, imdb_url, metacritic_url = get_imdb_metascore_ratings_and_synopsis(movie, year)
    tomatometer, tomatometer_votes, audience_score, audience_score_votes, rotten_tomatoes_url = get_rotten_tomatoes_ratings(movie, year)
    letterboxd, letterboxd_votes, letterboxd_url = get_letterboxd_rating(movie, year)
    tmdb, tmdb_votes, image, tmdb_url = get_tmdb_rating_and_movie_image(movie, year)
    # Close session after all scraping has occurred
    session.close()
    avg = get_average_rating(imdb, imdb_votes, metascore, metascore_votes, tomatometer, tomatometer_votes, audience_score, audience_score_votes, letterboxd, letterboxd_votes, tmdb, tmdb_votes)

    return movie_title, movie_year, imdb, imdb_votes, metascore, metascore_votes, synopsis, imdb_url, metacritic_url, tomatometer, tomatometer_votes, audience_score, audience_score_votes, rotten_tomatoes_url, letterboxd, letterboxd_votes, letterboxd_url, tmdb, tmdb_votes, image, tmdb_url, avg

"""
# Testing
movie = "the dirt"
year = '2019'

title, release_year, imdb, imdb_votes, metacritic, metacritic_votes, synopsis, imdb_url, metacritic_url, tomatometer, tomatometer_votes, audience, audience_score_votes, rotten_tomatoes_url, letterboxd, letterboxd_votes, letterboxd_url, tmdb, tmdb_votes, image, tmdb_url, avg = get_all_ratings(movie, year)

print("Title: " + title)
print("Year: " + release_year)
print("Synopsis: " + synopsis)
print("Movie Image: " + str(image))
print("Imdb: " + str(imdb))
print("Imdb votes:" + str(imdb_votes))
print("Imdb URL:" + str(imdb_url))
print("Metacritic: " + str(metacritic))
print("Metacritic votes:" + str(metacritic_votes))
print("Metacritic URL:" + str(metacritic_url))
print("Letterboxd: " + str(letterboxd))
print("Letterboxd votes:" + str(letterboxd_votes))
print("Letterboxd URL:" + str(letterboxd_url))
print("Tomatometer: " + str(tomatometer))
print("Tomatometer votes:" + str(tomatometer_votes))
print("Audience score: " + str(audience))
print("Audience score votes:" + str(audience_score_votes))
print("Rotten Tomatoes URL:" + str(rotten_tomatoes_url))
print("TMDB: " + str(tmdb))
print("TMDB votes:" + str(tmdb_votes))
print("TMDB URL:" + str(tmdb_url))
print("Average: " + str(avg))
"""
