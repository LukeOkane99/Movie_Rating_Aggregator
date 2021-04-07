def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='test-user36@gmail.com', password='reallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data
 
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data


def test_invalid_login_wrong_password(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is invalid
    """
    response = test_client.post('/login',
                                data=dict(email='test-user36@gmail.com', password='wrongreallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login unsuccessful, please check you have input the correct email and password!" in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">User Login</h1>' in response.data

def test_invalid_login_wrong_email(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid and flash message showing wrong details is displayed
    """
    response = test_client.post('/login',
                                data=dict(email='test-user3678@gmail.com', password='reallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login unsuccessful, please check you have input the correct email and password!" in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">User Login</h1>' in response.data

def test_invalid_login_empty_fields(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid and error message showing fields to be filled in is displayed
    """
    response = test_client.post('/login',
                                data=dict(email='', password='reallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">User Login</h1>' in response.data
    assert b'<input class="login-form-control" id="email" name="email" placeholder="Enter Your Email.." required type="text" value="">' in response.data
    assert b"<span>This field is required.</span>" in response.data

def test_logout_before_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check user is redirected to login page
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">User Login</h1>' in response.data

def test_login_when_already_logged_in(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='test-user36@gmail.com', password='reallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid and flash message pops up
    """
    response = test_client.post('/login',
                                data=dict(email='test-user36@gmail.com', password='reallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data
    assert b"You are already logged in with a registered account!" in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted (POST)
    THEN check user is successfully registered
    """
    response = test_client.post('/register',
                                data=dict(forename='testing',
                                          surname='user',
                                          email='test-user21@yahoo.com',
                                          password='test_password',
                                          password_confirmation='test_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Account successfully created. You can now log in!' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">User Login</h1>' in response.data


def test_duplicate_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted (POST)
    THEN check user registration is unsuccessful due to duplicate entry
    """
    response = test_client.post('/register',
                                data=dict(forename='Bob',
                                          surname='Dylan',
                                          email='test-user32@yahoo.com',
                                          password='bad_password',
                                          password_confirmation='bad_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Account successfully created. You can now log in!' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">User Login</h1>' in response.data

    response = test_client.post('/register',
                                data=dict(forename='Bob',
                                          surname='Dylan',
                                          email='test-user32@yahoo.com',
                                          password='bad_password',
                                          password_confirmation='bad_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'This email is in use, please use a different one!' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Register</h1>' in response.data

def test_registration_when_already_logged_in(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='test-user21@yahoo.com', password='test_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check flash message displaying user is already logged in is shown
    """
    response = test_client.get('/register')
    assert response.status_code == 302
    response = test_client.get('/movies/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data
    assert b"You are already logged in with a registered account!" in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_invalid_registration_different_passwords(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted (POST)
    THEN check user registeration is invalid and flash message is raised
    """
    response = test_client.post('/register',
                                data=dict(forename='James',
                                          surname='Smith',
                                          email='j-smith443@gmail.com',
                                          password='test_password',
                                          password_confirmation='different_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Field must be equal to password.' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Register</h1>' in response.data

def test_invalid_registration_email_already_exists(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted (POST)
    THEN check user registeration is invalid and flash message is raised
    """
    response = test_client.post('/register',
                                data=dict(forename='James',
                                          surname='Smith',
                                          email='test-user36@gmail.com',
                                          password='test_password',
                                          password_confirmation='test_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<input class="register-form-control" id="email" name="email" placeholder="Enter Your Email.." required type="text" value="test-user36@gmail.com">' in response.data
    assert b'This email is in use, please use a different one!' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Register</h1>' in response.data

def test_invalid_registration_invalid_email(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted (POST)
    THEN check user registeration is invalid and flash message is raised
    """
    response = test_client.post('/register',
                                data=dict(forename='James',
                                          surname='Smith',
                                          email='j-smith443',
                                          password='test_password',
                                          password_confirmation='test_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email address.' in response.data
    assert b'<input class="register-form-control" id="email" name="email" placeholder="Enter Your Email.." required type="text" value="j-smith443">' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Register</h1>' in response.data

def test_invalid_registration_empty_fields(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted (POST)
    THEN check user registeration is invalid and flash message is raised
    """
    response = test_client.post('/register',
                                data=dict(forename='James',
                                          surname='Smith',
                                          email='',
                                          password='',
                                          password_confirmation='test_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<input class="register-form-control" id="email" name="email" placeholder="Enter Your Email.." required type="text" value="">' in response.data
    assert b'<span style="color: whitesmoke; font-family: sans-serif; padding-bottom: 2rem; background-color: red;">This field is required.</span>' in response.data
    assert b'<input class="register-form-control" id="password" name="password" placeholder="Enter Your Password.." required type="password" value="">' in response.data
    assert b'<span>This field is required.</span>' in response.data

def test_viewing_profile_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='test-user36@gmail.com', password='reallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/1' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/1')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Profile Page</h1>' in response.data
    assert b'<input class="profile-form-control" id="email" name="email" required type="text" value="test-user36@gmail.com">' in response.data
    assert b'<input class="profile-form-control" id="forename" name="forename" required type="text" value="Test">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_updating_valid_details(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='test-user36@gmail.com', password='reallysecurepassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data
    
    """
    GIVEN a Flask application
    WHEN the '/users/1' page is posted to (POST)
    THEN check the response is valid and user details can be updated
    """
    response = test_client.post('/users/1',
                                data=dict(forename='Testing', surname='Account', email='test-user36@gmail.com'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Account details successfully updated!' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Profile Page</h1>' in response.data 
    assert b'<input class="profile-form-control" id="forename" name="forename" required type="text" value="Testing">' in response.data
    assert b'<input class="profile-form-control" id="surname" name="surname" required type="text" value="Account">' in response.data
    assert b'<input class="profile-form-control" id="email" name="email" required type="text" value="test-user36@gmail.com">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_updating_to_taken_email(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='swilliams-99@gmail.com', password='PaSsWoRd'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2' page is posted to (POST)
    THEN check the response is invalid and user email not updated to email already in use
    """
    response = test_client.post('/users/2',
                                data=dict(forename='Scott', surname='Williams', email='test-user36@gmail.com'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'This email is in use, please use a different one!' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Profile Page</h1>' in response.data 
    assert b'<input class="profile-form-control" id="forename" name="forename" required type="text" value="Scott">' in response.data
    assert b'<input class="profile-form-control" id="surname" name="surname" required type="text" value="Williams">' in response.data
    assert b'<input class="profile-form-control" id="email" name="email" required type="text" value="test-user36@gmail.com">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data


def test_updating_invalid_email(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='swilliams-99@gmail.com', password='PaSsWoRd'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2' page is posted to (POST)
    THEN check the response is invalid and user email not updated to new invalid email
    """
    response = test_client.post('/users/2',
                                data=dict(forename='Scott', surname='Williams', email='swilliams-99'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid email address.' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Profile Page</h1>' in response.data 
    assert b'<input class="profile-form-control" id="forename" name="forename" required type="text" value="Scott">' in response.data
    assert b'<input class="profile-form-control" id="surname" name="surname" required type="text" value="Williams">' in response.data
    assert b'<input class="profile-form-control" id="email" name="email" required type="text" value="swilliams-99">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_accessing_watchlist_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='swilliams-99@gmail.com', password='PaSsWoRd'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2/watchlist' page is requested to (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/2/watchlist')
    assert response.status_code == 200
    assert b'<li><a href="/users/2/watchlist", style="padding-left: 0.5rem;">Watchlist' in response.data
    assert b'<h1 class="page_tites">Watchlist</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_adding_movie_to_watchlist(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='swilliams-99@gmail.com', password='PaSsWoRd'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2/watchlist/add/movies/1/Gladiator_2000' route is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/users/2/watchlist/add/movies/1/Gladiator_2000')
    assert response.status_code == 302
    
    """
    GIVEN a Flask application
    WHEN the '/users/2/watchlist' page is requested to (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/2/watchlist')
    assert response.status_code == 200
    assert b'<li><a href="/users/2/watchlist", style="padding-left: 0.5rem;">Watchlist' in response.data
    assert b'<h1 class="page_tites">Watchlist</h1>' in response.data
    assert b"Gladiator (2000)" in response.data
    assert b"86.9" in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_removing_movie_from_watchlist(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='swilliams-99@gmail.com', password='PaSsWoRd'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">Login successful!</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2/watchlist' page is requested to (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/2/watchlist')
    assert response.status_code == 200
    assert b'<li><a href="/users/2/watchlist", style="padding-left: 0.5rem;">Watchlist' in response.data
    assert b'<h1 class="page_tites">Watchlist</h1>' in response.data
    assert b"Gladiator (2000)" in response.data
    assert b"86.9" in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2/watchlist/delete/movies/1/Gladiator_2000' route is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/users/2/watchlist/delete/movies/1/Gladiator_2000')
    assert response.status_code == 302

    """
    GIVEN a Flask application
    WHEN the '/users/2/watchlist' page is requested to (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/2/watchlist')
    assert response.status_code == 200
    assert b'<li><a href="/users/2/watchlist", style="padding-left: 0.5rem;">Watchlist' in response.data
    assert b'<h1 class="page_tites">Watchlist</h1>' in response.data
    assert b"Gladiator (2000)" not in response.data
    assert b"86.9" not in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data