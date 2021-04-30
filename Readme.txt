Steps to run the project:

1. Ensure Docker and Docker compose are installed. (Docker Desktop comes with Docker Compose included)
2. Navigate to the root directory of the project
3. In the terminal run 'docker-compose build' to build all containers - this may take some time!
4. To run the website container when all containers have been built
run the command 'docker compose up web'.
When the container has started, navigate to http://localhost:5000/ to access the website.
5. To access the update script to update all movies in the database, run the command 'docker compose up update-script'
6. To run the unit tests for the project, run the command 'docker compose up tests' 

Other Notes:

To access the super user admin account for the site use the following login details:
email: super-user@test.com
password: testing123

When searching for a movie not in the database, the exact title and year for the film are required.