def test_landing_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"All Movies" in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_all_movies_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_high_to_low_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/hightolow' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/hightolow')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">High to Low Ratings</h1>' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_high_to_low_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/lowtohigh' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/lowtohigh')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Low to High Ratings</h1>' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_favourable_page(test_client, init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/favourable' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/favourable')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Favourable Ratings</h1>' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_non_favourable_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/non-favourable' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/non-favourable')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Non-Favourable Ratings</h1>' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' not in response.data

def test_top10_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/top10' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/top10')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Top 10 Movies</h1>' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_search_by_year_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/year' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/year')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Search movies by year</h1>' in response.data

def test_searching_for_valid_movie(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/movies/results/Gladiator' route is posted (POST)
    THEN check the response is valid
    """
    response = test_client.post('/movies/results/Gladiator')
    assert response.status_code == 200
    assert b"1 Result found for search \'Gladiator\'" in response.data
    assert b'<a href="/movies/Gladiator_2000" style="display: inline-block;">' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_searching_for_movie_not_present(test_client, init_database):
    response = test_client.post('/movies/results/Tenet')
    assert response.status_code == 200
    assert b"0 Results found for search \'Tenet\'" in response.data
    assert b'<a href="/movies/Tenet_2020" style="display: inline-block;">' not in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Tenet (2020)</br></div>' not in response.data

def test_searching_for_movie_with_partial_title(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/movies/results/glad' route is posted (POST)
    THEN check the response is valid
    """
    response = test_client.post('/movies/results/glad')
    assert response.status_code == 200
    assert b"1 Result found for search \'glad\'" in response.data
    assert b'<a href="/movies/Gladiator_2000" style="display: inline-block;">' in response.data
    assert b'<div style=" font-size: 1.1rem; float: left;">Gladiator (2000)</br></div>' in response.data

def test_scraping_new_movie(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/movies/Tenet_2020' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/Tenet_2020')
    assert response.status_code == 200
    assert b"<b>Tenet</b> (2020)" in response.data
    assert b"""Armed with only one word, Tenet, and fighting for the survival of the entire world, a Protagonist journeys through a twilight world of international espionage on a mission that will unfold in something beyond real time.""" in response.data
    assert b'<div class="rating-circle movie-page-rating-circle">' in response.data
    assert b"IMDb:" in response.data
    assert b"Metascore:" in response.data
    assert b"Tomatometer:" in response.data
    assert b"Audience Score:" in response.data
    assert b"Letterboxd:" in response.data
    assert b"TMDb:" in response.data

def test_scraping_invalid_movie(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/movies/results/Batman_2030' page is requested (GET)
    THEN check the response is invalid
    """
    response = test_client.get('/movies/results/Batman_2030')
    assert response.status_code == 200 or response.status_code == 302
    assert b"Refine your search for better results" in response.data
    assert b"0 Results found for search \'Batman 2030\'" in response.data

def test_searching_movies_by_year(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/movies/year/2000' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/year/2000')
    assert response.status_code == 200
    assert b"1 Result found for year \'2000\'" in response.data
    assert b"Gladiator (2000)" in response.data
    assert b"86.9"

def test_searching_movies_by_year_no_results(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/movies/year/2019' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/year/2019')
    assert response.status_code == 200
    assert b"0 Results found for year \'2019\'" in response.data
    assert b'<h1 class="page_tites">Search movies by year</h1>'

