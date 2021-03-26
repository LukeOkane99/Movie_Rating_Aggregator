# Test getting pages
def test_landing_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"All Movies" in response.data

def test_all_movies_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_high_to_low_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/hightolow' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/hightolow')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">High to Low Ratings</h1>' in response.data

def test_high_to_low_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/lowtohigh' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/lowtohigh')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Low to High Ratings</h1>' in response.data

def test_favourable_page(test_client, init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/favourable' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/favourable')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Favourable Ratings</h1>' in response.data

def test_non_favourable_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/non-favourable' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/non-favourable')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Non-Favourable Ratings</h1>' in response.data

def test_top10_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/top10' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/top10')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Top 10 Movies</h1>' in response.data

def test_search_by_year_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/movies/year' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/movies/year')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">Search movies by year</h1>' in response.data

def test_help_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/help' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/help')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 1rem;">Help</h1>' in response.data
    assert b'<h2 style="margin-left: auto; margin-right: auto; width: 60%; font-family: sans-serif; color: whitesmoke;">What is the goal of this site?</h2>' in response.data

def test_register_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Register</h1>' in response.data
    assert b'<a href="/login" class="all-small">Already have an account?</a>' in response.data

def test_login_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">User Login</h1>' in response.data
    assert b'<a href="/reset_password" class="all-small">Forgot your password?</a>' in response.data

def test_reset_password_page(test_client , init_database):
    """
    GIVEN a an application configured for testing
    WHEN the '/reset_password' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/reset_password')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Request Password Reset</h1>' in response.data
    assert b'<input class="login-form-button" id="request_reset_button" name="request_reset_button" type="submit" value="Request Password Reset">' in response.data
