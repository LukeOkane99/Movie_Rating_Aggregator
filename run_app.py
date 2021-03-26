from rating_aggregator import create_app
from rating_aggregator.config import Config

app = create_app(config_class=Config)

# run application
if __name__ == '__main__':
    app.run(debug=True)