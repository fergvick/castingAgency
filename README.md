Casting Agency
---------------

### Motivation
This is the final project for the Udacity Full Stack Developer Nanodegree

### Dependencies
Install all dependencies by running
`pip3 install -r requirements.txt`

### Initiallization
TO start the app, first run:
`source setup.sh`
then
`flask run`

### Login Details
To login or sign up for an account, go to the following URL;
`https://udacity-casting-agency.eu.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=LC7SXH3s1ZRzI0bAHzWnhSYFOagXN6ye&redirect_uri=http://127.0.0.1:5000`
Then copy the JWT access_token to be used as a Bearer Authentication Token for API requests
For each role these are the login details

#### Casting Assistant
Email: 
`assistant@casting.com`

Password: 
`Assistant123`

#### Casting Director
Email: 
`director@casting.com`

Password: 
`Director123`

#### Executive Producer
Email: 
`producer@casting.com`

Password: 
`Producer123`

Auth0 details can by found in `setup.sh`

### Endpoints

#### GET /actors

#### POST /actors

#### PATCH /actors/<int:id>

#### DELETE /actors/<int:id>

#### GET /movies

#### POST /movies

#### PATCH /movies/<int:id>

#### DELETE /movies/<int:id>

### Testing
Run `python3 test_app.py`