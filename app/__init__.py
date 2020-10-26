from flask import Flask

# Create app package
app = Flask(__name__)

from app import routes