# Initialise application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Create app instance
app = Flask(__name__)

# protect against modifying cookies and forgery attacks
app.config["SECRET_KEY"] = 'dab516ff56bff14979aa4568b1fd78ba'

# Set location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Relative path for database
# Create instance of database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Handle logged in user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# import routes after app is initialised
from rating_aggregator import routes