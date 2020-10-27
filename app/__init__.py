from flask import Flask

# Create app package
app = Flask(__name__)
app.config["DEBUG"] = True

from app import routes