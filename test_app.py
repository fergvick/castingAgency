import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from datetime import datetime

assistant_token = os.getenv('ASSISTANT_TOKEN')
director_token = os.getenv('DIRECTOR_TOKEN')
producer_token = os.getenv('PRODUCER_TOKEN')

def set_auth_header(role):
    if role == 'assistant':
        return {'Authorization': 'Bearer {}'.format(assistant_token)}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(director_token)}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(producer_token)}


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "d1gh16kqs0coa8.db"
        self.database_path = os.getenv('DATABASE_URL')
        setup_db(self.app, self.database_path)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'test actor',
            'age': 23,
            'gender': 'Female'
        }

        self.new_movie = {
            'title': 'test movie',
            'release_date': 230323
        }

    def tearDown(self):
        """Executed after reach test"""
        pass


    ## ACTORS ENDPOINTS TESTS
    """
    Test for successful GET request at /actors endpoint
    """
    def test_get_actors(self):
        res = self.client().get('/actors', headers=set_auth_header('assistant'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])

    """
    Test for unauthorized GET request at /actors endpoint
    """
    def test_get_actors_unauthorized(self):
        res = self.client().get('/actors', headers=set_auth_header(''))

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    """
    Test for successful POST request at /actors endpoint to create a new actor
    """
    def test_create_new_actor(self):
        res = self.client().post('/actors', headers=set_auth_header('director'), json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    """
    Test for failed POST request at /actors endpoint when a argument is missing from the actors JSON object
    """
    def test_400_if_missing_json_object(self):
        res = self. client(). post('/actors', headers=set_auth_header('director'), json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    """
    Test for unauthorized GET request at /actors endpoint
    """
    def test_create_actor_unauthorized(self):
        res = self.client().post('/actors', headers=set_auth_header(''), json=self.new_actor)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    """
    Test for successful PATCH request at /actors endpoint to create a new actor
    """
    def test_edit_actor(self):
        res = self.client().post('/actors', headers=set_auth_header('director'), json=self.new_actor)
        actor_id = Actor.query.first().id
        res = self.app.patch(f'/actors/{actor_id}', headers=set_auth_header('director'), json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    """
    Test for unauthorized PATCH request at /actors endpoint to create a new actor
    """
    def test_edit_actor_unauthorized(self):
        res = self.client().post('/actors', headers=set_auth_header('director'), json=self.new_actor)
        actor_id = Actor.query.first().id
        res = self.app.patch(f'/actors/{actor_id}', headers=set_auth_header('assistant'), json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    """
    Test for successful DELETE request at /actors endpoint for actor id = 10
    """
    def test_delete_actors(self):
        res = self.client().post('/actors', headers=set_auth_header('director'), json=self.new_actor)
        actor_id = Actor.query.first().id
        res = self.client().delete(f'/actors/{actor_id}', headers=set_auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)

    """
    Test for failed DELETE request at /actors endpoint a actor that doesn't exist
    """
    def test_delete_actors_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers=set_auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable')

    """
    Test for unauthorized DELETE request at /actors endpoint
    """
    def test_delete_actors_unauthorized(self):
        res = self.client().post('/actors', headers=set_auth_header('director'), json=self.new_actor)
        actor_id = Actor.query.first().id
        res = self.client().delete(f'/actors/{actor_id}', headers=set_auth_header('assistant'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')


    ## MOVIES ENDPOINTS TESTS
        """
    Test for successful GET request at /movies endpoint
    """
    def test_get_movies(self):
        res = self.client().get('/movies', headers=set_auth_header('assistant'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])

    """
    Test for unauthorized GET request at /movies endpoint
    """
    def test_get_movies_unauthorized(self):
        res = self.client().get('/movies', headers=set_auth_header(''))

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    """
    Test for successful POST request at /movies endpoint to create a new movie
    """
    def test_create_new_movie(self):
        res = self.client().post('/movies', headers=set_auth_header('producer'), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    """
    Test for failed POST request at /movies endpoint when a argument is missing from the movies JSON object
    """
    def test_400_if_missing_json_object(self):
        res = self. client(). post('/movies', headers=set_auth_header('producer'), json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    """
    Test for unauthorized GET request at /movies endpoint
    """
    def test_create_movie_unauthorized(self):
        res = self.client().get('/movies', headers=set_auth_header('director'), json=self.new_movie)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    """
    Test for successful PATCH request at /movies endpoint to create a new movie
    """
    def test_edit_movie(self):
        res = self.client().post('/movies', headers=set_auth_header('director'), json=self.new_movie)
        movie_id = Movie.query.first().id
        res = self.app.patch(f'/movies/{movie_id}', headers=set_auth_header('director'), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    """
    Test for unauthorized PATCH request at /movies endpoint to create a new movie
    """
    def test_edit_movie_unauthorized(self):
        res = self.client().post('/movies', headers=set_auth_header('director'), json=self.new_movie)
        movie_id = Movie.query.first().id
        res = self.app.patch(f'/movies/{movie_id}', headers=set_auth_header('assistant'), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    """
    Test for successful DELETE request at /movies endpoint for movie id = 10
    """
    def test_delete_movies(self):
        res = self.client().post('/movies', headers=set_auth_header('director'), json=self.new_movie)
        movie_id = Movie.query.first().id
        res = self.client().delete(f'/movies/{movie_id}', headers=set_auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)

    """
    Test for failed DELETE request at /movies endpoint a movie that doesn't exist
    """
    def test_delete_movies_does_not_exist(self):
        res = self.client().post('/movies', headers=set_auth_header('director'), json=self.new_movie)
        movie_id = Movie.query.first().id
        res = self.client().delete('/movies/1000', headers=set_auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable')

    """
    Test for unauthorized DELETE request at /movies endpoint 
    """
    def test_delete_actors_unauthorized(self):
        res = self.client().post('/movies', headers=set_auth_header('director'), json=self.new_movie)
        movie_id = Movie.query.first().id
        res = self.client().delete(f'/movies/{movie_id}', headers=set_auth_header('director'))       
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
