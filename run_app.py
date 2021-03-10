from rating_aggregator import create_app

app = create_app()

# run application
if __name__ == '__main__':
    app.run(debug=True)