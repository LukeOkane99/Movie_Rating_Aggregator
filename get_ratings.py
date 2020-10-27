from bs4 import BeautifulSoup
import requests
from requests import get, Session
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import re
import lxml
import time
import cchardet

movie = "tenet"
year = "2020"

session = Session()

def get_imdb_metacritic_ratings(movie, year):
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
        return float(imdb_rating), float(metacritic_rating)

def get_letterboxd_rating(movie, year):
    try:
        response = session.get("https://letterboxd.com/search/films/"+movie+" "+year)
        if response.status_code == 200:
            bs_object = BeautifulSoup(response.content, 'lxml')
            titles = bs_object.find_all('span', class_ = "film-title-wrapper")
            for title in titles:
                # Split string into substrings based on title and year
                ttl,yr = title.text.rsplit(' ', 1)
                if movie == ttl.lower() and yr in year:  
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
            return rating

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
        return tmdb_rating

def get_average_rating(imdb, metascore, letterboxd, tomatometer, audience_score, tmdb):
    avg_rating = ((imdb*10)+metascore+(letterboxd*20)+tomatometer+audience_score+(tmdb*10)) / 6
    avg_rating = round(avg_rating, 1)
    return avg_rating

#imdb, metascore = get_imdb_metacritic_ratings(movie, year)
#letterboxd = get_letterboxd_rating(movie, year)
#tomatometer, audience_score = get_rotten_tomatoes_ratings(movie, year)
#tmdb = get_tmdb_rating(movie, year)
#print(get_average_rating(imdb, metascore, letterboxd, tomatometer, audience_score, tmdb))

"""
def get_roger_ebert_rating(movie, year):
    # Set headless broswer option for chrome driver
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('C:\\bin\\chromedriver.exe', options = options)

    # Search for moie title and click on relevant review page.
    search_url = r"https://www.rogerebert.com/search?utf8=r%E2%9C%93&q="+movie+" "+year
    driver.get(search_url)
    search_results = driver.find_elements_by_xpath("//a[@class='gs-title']")
    string1 = movie + " movie review (" + year + ")"
    string2 = movie + " movie review & film summary (" + year + ")"
    for result in search_results:
        if string1.lower() in result.text.lower() or string2.lower() in result.text.lower():
            result.send_keys(Keys.ENTER) 
            break 

    # get movie star rating element          
    bs_object = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    star_container = bs_object.find_all('span', class_ = "star-rating _large")

    star_rating = 0
    percentage_rating = 0
    # Determine star rating and convert to percentage
    for star in star_container[0].contents:
        if "star-full" in str(star):
            star_rating += 1
            percentage_rating += 25
        elif "star-half" in str(star):
            star_rating += 0.5
            percentage_rating += 12.5 
    return star_rating
"""