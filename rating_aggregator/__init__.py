# Initialise application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from rating_aggregator.config import Config

# Create instance of database
db = SQLAlchemy()
bcrypt = Bcrypt()

# Handle logged in user sessions
login_manager = LoginManager()
login_manager.login_view = 'users.login'

mail = Mail()

# Function allows to create different instances of the app
# With different configurations
def create_app(config_class=Config):
    # Create app instance
    app = Flask(__name__)

    # Config for app
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import routes from blueprints after app is initialised
    from rating_aggregator.users.routes import users
    from rating_aggregator.movies.routes import movies
    from rating_aggregator.main.routes import main
    from rating_aggregator.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(movies)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
