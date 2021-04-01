from flask_login import current_user

def test_admin_page_accessible_as_admin(test_client, init_database):
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
    assert current_user.admin == True

    """
    GIVEN a Flask application
    WHEN the '/users/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">All Users</h1>' in response.data
    assert b'<th>USER ID</th>' in response.data
    assert b'<td>2</td>' in response.data
    assert b'<th style="width: 15%;">FORENAME</th>' in response.data
    assert b'<td style="width: 15%;">Scott</td>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data


def test_admin_page_not_accessible_as_regular_user(test_client, init_database):
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
    assert current_user.admin == False

    """
    GIVEN a Flask application
    WHEN the '/users/all' page is requested (GET)
    THEN check the response is invalid
    """
    response = test_client.get('/users/all')
    assert response.status_code == 403
    assert b'Oops.. This Page is forbidden!' in response.data
    assert b'<h1 style="text-align: center; font-family: sans-serif; color: whitesmoke; font-size: 200px;">403</h1>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_making_user_admin(test_client, init_database):
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
    assert current_user.admin == True

    """
    GIVEN a Flask application
    WHEN the '/users/2/admin=True' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/users/2/admin=True')
    assert response.status_code == 302

    """
    GIVEN a Flask application
    WHEN the '/users/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">All Users</h1>' in response.data
    assert b'<th>USER ID</th>' in response.data
    assert b'<td>2</td>' in response.data
    assert b'<th style="width: 15%;">FORENAME</th>' in response.data
    assert b'<td style="width: 15%;">Scott</td>' in response.data
    assert b'<input type=submit class="deletebtn" value="Remove Admin">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data
    
def test_removing_user_admin(test_client, init_database):
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
    assert current_user.admin == True

    """
    GIVEN a Flask application
    WHEN the '/users/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">All Users</h1>' in response.data
    assert b'<th>USER ID</th>' in response.data
    assert b'<td>2</td>' in response.data
    assert b'<th style="width: 15%;">FORENAME</th>' in response.data
    assert b'<td style="width: 15%;">Scott</td>' in response.data
    assert b'<input type=submit class="deletebtn" value="Remove Admin">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2/admin=False' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/users/2/admin=False')
    assert response.status_code == 302

    """
    GIVEN a Flask application
    WHEN the '/users/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">All Users</h1>' in response.data
    assert b'<th>USER ID</th>' in response.data
    assert b'<td>2</td>' in response.data
    assert b'<th style="width: 15%;">FORENAME</th>' in response.data
    assert b'<td style="width: 15%;">Scott</td>' in response.data
    assert b'<input type=submit class="deletebtn" value="Make Admin">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_editing_admin(test_client, init_database):
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
    assert current_user.admin == True

    """
    GIVEN a Flask application
    WHEN the '/users/1' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/1')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Profile Page</h1>' in response.data 
    assert b'<input class="profile-form-control" id="forename" name="forename" required type="text" value="Test">' in response.data
    assert b'<input class="profile-form-control" id="surname" name="surname" required type="text" value="User">' in response.data
    assert b'<input class="profile-form-control" id="email" name="email" required type="text" value="test-user36@gmail.com">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/1' page is posted to (POST)
    THEN check the response is valid and user details successfully updated
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

def test_editing_other_user(test_client, init_database):
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
    assert current_user.admin == True

    """
    GIVEN a Flask application
    WHEN the '/users/2' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/2')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Profile Page</h1>' in response.data 
    assert b'<input class="profile-form-control" id="forename" name="forename" required type="text" value="Scott">' in response.data
    assert b'<input class="profile-form-control" id="surname" name="surname" required type="text" value="Williams">' in response.data
    assert b'<input class="profile-form-control" id="email" name="email" required type="text" value="swilliams-99@gmail.com">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2' page is posted to (POST)
    THEN check the response is valid and user details successfully updated
    """
    response = test_client.post('/users/2',
                                data=dict(forename='Scotty', surname='Williams', email='s-williams-9988@gmail.com'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Account details successfully updated!' in response.data
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">Profile Page</h1>' in response.data 
    assert b'<input class="profile-form-control" id="forename" name="forename" required type="text" value="Scotty">' in response.data
    assert b'<input class="profile-form-control" id="surname" name="surname" required type="text" value="Williams">' in response.data
    assert b'<input class="profile-form-control" id="email" name="email" required type="text" value="s-williams-9988@gmail.com">' in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data

def test_deleting_user(test_client, init_database):
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
    assert current_user.admin == True

    """
    GIVEN a Flask application
    WHEN the '/users/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">All Users</h1>' in response.data
    assert b'<th>USER ID</th>' in response.data
    assert b'<td>2</td>' in response.data
    assert b'<th style="width: 15%;">FORENAME</th>' in response.data
    assert b'<td style="width: 15%;">Scotty</td>' in response.data
    assert b'<th style="width:20%;">EMAIL</th>' in response.data
    assert b'<td style="width: 20%;">s-williams-9988@gmail.com</td>' in response.data

    """
    GIVEN a Flask application
    WHEN the '/users/2/delete' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/users/2/delete')
    assert response.status_code == 302

    """
    GIVEN a Flask application
    WHEN the '/users/all' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/users/all')
    assert response.status_code == 200
    assert b'<h1 class="page_tites" style="padding-bottom: 2rem;">All Users</h1>' in response.data
    assert b'<th>USER ID</th>' in response.data
    assert b'<td>2</td>' not in response.data
    assert b'<th style="width: 15%;">FORENAME</th>' in response.data
    assert b'<td style="width: 15%;">Scott</td>' not in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'<div id="flash-messages" class="flash-success">User successfully logged out</div>' in response.data
    assert b'<h1 class="page_tites">All Movies</h1>' in response.data
