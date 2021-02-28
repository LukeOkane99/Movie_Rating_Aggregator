from bs4 import BeautifulSoup
from rating_aggregator import app, db
from rating_aggregator.models import Movie
import requests
from requests import get, Session
import json
import re
import lxml
import time
import cchardet
from multiprocessing import Pool
from datetime import datetime

def scrape_top_level_urls(url):
    if 'metacritic' in url:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        return response

def main():
    print('**** Starting Update Process... ****')

    movies = Movie.query.all()
    for movie in movies:
        difference = datetime.utcnow() - movie.date_updated
        if difference.days != 0:
            name = movie.title
            year = movie.year

            imdb_url = r"https://www.imdb.com/search/title/?title="+name+"+&title_type=feature"
            metacritic_url = "https://www.metacritic.com/search/movie/"+name+"/results"
            letterboxd_url = "https://letterboxd.com/search/films/"+name+" "+year
            rotten_tomatoes_url = r"https://www.rottentomatoes.com/search?search="+name
            tmdb_url = 'https://api.themoviedb.org/3/search/movie?api_key=35847ff7af4ea4159527ddec5fa4a2f4&query='+name+'&year='+year

            top_level_urls = [imdb_url, metacritic_url, letterboxd_url, rotten_tomatoes_url, tmdb_url]

            p = Pool(5)
            responses = p.map(scrape_top_level_urls, top_level_urls)
            p.terminate()
            p.join()
            
            #--------------------------------------Check if movie votes and ratings need updated--------------------------------------------------#

            print("**** "+name+" ("+year+")"+" ****")
            session = Session()

            for response in responses:
                if response is not None:
                    if 'imdb' in response.url:
                        imdb_rating = None
                        imdb_votes = None
                        metacritic_rating = None
                        try:
                            bs_object = BeautifulSoup(response.content, 'lxml')
                            titles = bs_object.find_all('div', class_ = "lister-item-content")
                            for title in titles:
                                movie_title = title.find_all('a')[0].get_text()
                                movie_year = title.find('span', class_ = 'lister-item-year text-muted unbold').get_text()
                                if '(I' in movie_year and year in movie_year:
                                    movie_year = movie_year.split(' ')
                                    movie_year = movie_year[1]
                                movie_year = movie_year.replace('(', '').replace(')', '')
                                if movie_title.lower() == name.lower() and year in movie_year:
                                    if title.find('div', class_='inline-block ratings-imdb-rating'):
                                        imdb_rating = (float(title.find('div', class_='inline-block ratings-imdb-rating').get('data-value'))*10)
                                        spans = title.find('p', class_='sort-num_votes-visible').find_all('span')
                                        imdb_votes = int(spans[1].get('data-value'))
                                    if title.find('div', class_ = 'inline-block ratings-metascore'):
                                        metacritic_rating = float(title.find('div', class_ = 'inline-block ratings-metascore').span.text.strip()) 
                                    break
                            if imdb_rating is not None and imdb_rating != movie.imdb_rating:
                                movie.imdb_rating = imdb_rating
                                db.session.commit()
                                print('imdb rating updated')
                            elif imdb_rating == movie.imdb_rating: 
                                print('imdb rating is the same')
                            if imdb_votes is not None and imdb_votes != movie.imdb_votes:
                                movie.imdb_votes = imdb_votes
                                db.session.commit()
                                print('imdb votes updated')
                            elif imdb_votes == movie.imdb_votes: 
                                print('imdb votes are the same')
                            if metacritic_rating is not None and metacritic_rating != movie.metascore:
                                movie.metascore = metacritic_rating
                                db.session.commit()
                                print('metascore updated')
                            elif metacritic_rating == movie.metascore: 
                                print('metascore is the same')
                        except Exception as ex:
                            print(str(ex)) 
                            continue
                    elif 'metacritic' in response.url:
                        matacritic_votes = None
                        try:
                            bs_object = BeautifulSoup(response.content, 'lxml')
                            titles = bs_object.find_all('div', class_ = "main_stats")
                            for title in titles:
                                movie_title = title.find('a').get_text().strip()
                                movie_year = title.find('p').get_text().strip().split(' ')
                                movie_year = movie_year[1]
                                if movie_title.lower() == name.lower() and movie_year == year:
                                    endpoint = title.find('a').get('href')
                                    headers = {
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
                                    }
                                    response = session.get('https://www.metacritic.com'+endpoint, headers=headers)
                                    bs_object = BeautifulSoup(response.content, 'lxml')
                                    info = bs_object.find('script', type='application/ld+json')
                                    if json.loads(info.string)['aggregateRating']['ratingValue']:
                                        metacritic_votes = int(json.loads(info.string)['aggregateRating']['ratingCount'])
                                        break
                            if metacritic_votes is not None and metacritic_votes != movie.metascore_votes:
                                movie.imdb_votes = imdb_votes
                                db.session.commit()
                                print('metascore votes updated')
                            elif metacritic_votes == movie.metascore_votes: 
                                print('metascore votes are the same')
                        except Exception as ex:
                            print(str(ex)) 
                            continue
                    elif 'letterboxd' in response.url:
                        rating = None
                        letterboxd_votes = None
                        try:
                            bs_object = BeautifulSoup(response.content, 'lxml')
                            titles = bs_object.find_all('span', class_ = "film-title-wrapper")
                            for title in titles:
                                # Split string into substrings based on title and year
                                ttl,yr = title.text.rsplit(' ', 1)
                                if name.lower() == str(ttl.lower()) and str(yr) in year: 
                                    review_endpoint = title.find('a').get('href')
                                    break
                            response = session.get("https://letterboxd.com"+review_endpoint)
                            if response.status_code == 200:
                                bs_object = BeautifulSoup(response.content, 'lxml')
                                info = bs_object.find_all('script', type='application/ld+json')[0]
                                # parse json inside script tag and use regex to return only the dict
                                if json.loads( re.search(r'({.*})', info.string).group() )['aggregateRating']['ratingValue']:
                                    rating = round((json.loads( re.search(r'({.*})', info.string).group() )['aggregateRating']['ratingValue'] * 20), 1)
                                    letterboxd_votes = int(json.loads( re.search(r'({.*})', info.string).group() )['aggregateRating']['ratingCount'])
                            if rating is not None and rating != movie.letterboxd_rating:
                                movie.letterboxd_rating = rating
                                db.session.commit()
                                print('letterboxd rating updated')
                            elif rating == movie.letterboxd_rating: 
                                print('letterboxd rating is the same')
                            if letterboxd_votes is not None and letterboxd_votes != movie.letterboxd_votes:
                                movie.letterboxd_votes = letterboxd_votes
                                db.session.commit()
                                print('letterboxd votes updated')
                            elif letterboxd_votes == movie.letterboxd_votes: 
                                print('letterboxd votes are the same')
                        except Exception as ex:
                            print(str(ex)) 
                            continue
                    elif 'rottentomatoes' in response.url:
                        tomatometer_score = None
                        tomatometer_votes = None
                        audience_score = None
                        audience_score_votes = None
                        try:
                            bs_object = BeautifulSoup(response.content, 'lxml')
                            dicts = bs_object.find_all('script', type='application/json', id='movies-json')[0]
                            info = json.loads( re.search(r'({.*})', dicts.string).group() )
                            for item in info['items']:
                                if item['name'].lower() == name.lower() and item['releaseYear'] == year:
                                    url = item['url']
                                    response = session.get(url)
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
                            if tomatometer_score is not None and tomatometer_score != movie.tomatometer:
                                movie.tomatometer = tomatometer_score
                                db.session.commit()
                                print('tomatometer score updated')
                            elif tomatometer_score == movie.tomatometer: 
                                print('tomatometer score is the same')
                            if tomatometer_votes is not None and tomatometer_votes != movie.tomatometer_votes:
                                movie.tomatometer_votes = tomatometer_votes
                                db.session.commit()
                                print('tomatometer votes updated')
                            elif tomatometer_votes == movie.tomatometer_votes: 
                                print('tomatometer votes are the same')
                            if audience_score is not None and audience_score != movie.audience_score:
                                movie.audience_score = audience_score
                                db.session.commit()
                                print('audience score updated')
                            elif audience_score == movie.audience_score: 
                                print('audience score is the same')
                            if audience_score_votes is not None and audience_score_votes != movie.audience_score_votes:
                                movie.audience_score_votes = audience_score_votes
                                db.session.commit()
                                print('audience score votes updated')
                            elif audience_score_votes == movie.audience_score_votes: 
                                print('audience score votes are the same')
                        except Exception as ex:
                            print(str(ex)) 
                            continue
                    elif 'themoviedb' in response.url:
                        tmdb_rating = None
                        tmdb_votes = None
                        try:
                            for film in response.json()['results']:
                                if film['title'].lower() == name.lower() and year in film['release_date']:
                                    if film['vote_average']:
                                        tmdb_rating = (film['vote_average']*10)
                                        tmdb_votes = int(film['vote_count'])
                            if tmdb_rating is not None and tmdb_rating != movie.tmdb_rating:
                                movie.tmdb_rating = tmdb_rating
                                db.session.commit()
                                print('tmdb rating updated')
                            elif tmdb_rating == movie.tmdb_rating: 
                                print('tmdb rating is the same')
                            if tmdb_votes is not None and tmdb_votes != movie.tmdb_votes:
                                movie.tmdb_votes = tmdb_votes
                                db.session.commit()
                                print('tmdb votes updated')
                            elif tmdb_votes != movie.tmdb_votes: 
                                print('tmdb votes are the same')
                        except Exception as ex:
                            print(str(ex)) 
                            continue
                
                session.close()

            #--------------------------Calculate new weighted average--------------------------------------------------#

            all_votes = [movie.imdb_votes, movie.metascore_votes, movie.letterboxd_votes, movie.tomatometer_votes, movie.audience_score_votes, movie.tmdb_votes]
            existing_votes = []
            for votes in all_votes:
                if votes is not None:
                    existing_votes.append(votes)
                    total_votes = sum(existing_votes)

            weighted_scores = []

            if movie.imdb_rating is not None and movie.imdb_votes is not None:
                imdb_weighted = (movie.imdb_rating*movie.imdb_votes)
                weighted_scores.append(imdb_weighted)
            if movie.metascore is not None and movie.metascore_votes is not None:
                meta_weighted = (movie.metascore*movie.metascore_votes)
                weighted_scores.append(meta_weighted)
            if movie.letterboxd_rating is not None and movie.letterboxd_votes is not None:
                letterboxd_weighted = (movie.letterboxd_rating*movie.letterboxd_votes)
                weighted_scores.append(letterboxd_weighted)
            if movie.tomatometer is not None and movie.tomatometer_votes is not None:
                tomatometer_weighted = (movie.tomatometer*movie.tomatometer_votes)
                weighted_scores.append(tomatometer_weighted)
            if movie.audience_score is not None and movie.audience_score_votes is not None:
                audience_score_weighted = (movie.audience_score*movie.audience_score_votes)
                weighted_scores.append(audience_score_weighted)
            if movie.tmdb_rating is not None and movie.tmdb_votes is not None:
                tmdb_weighted = (movie.tmdb_rating*movie.tmdb_votes)
                weighted_scores.append(tmdb_weighted)

            product_of_rating_and_votes = sum(weighted_scores)
            weighted_rating = product_of_rating_and_votes / total_votes
            weighted_rating = round(weighted_rating, 1)

            if movie.average_rating != weighted_rating:
                movie.average_rating = weighted_rating
                print('weighted average updated')
            else:
                print('weighted average is the same')
            print('\n')
            
            movie.date_updated = datetime.utcnow()

    print('**** Update Process Completed! ****')

if __name__ ==  '__main__':
    main()
