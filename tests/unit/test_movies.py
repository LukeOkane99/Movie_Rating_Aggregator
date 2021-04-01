def test_searching_for_valid_movie(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/movies/results/Gladiator' page is posted (POST)
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
    WHEN the '/movies/results/glad' page is posted (POST)
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