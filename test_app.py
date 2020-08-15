import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from datetime import datetime

# assistant@casting.com Assistant123
assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilc5bTVEM3FEQ1Etc3BUcWFlVldPeiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2FzdGluZy1hZ2VuY3kuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzU5ZGQ4MTcwNGFmMDA2ZGRmMjhjMSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTk3NDkwMDYwLCJleHAiOjE1OTc0OTcyNjAsImF6cCI6IkxDN1NYSDNzMVpSekkwYkFIelduaFNZRk9hZ1hONnllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.lIAQH85n-V9ii4eFUOVfqx-1oujSzxH1GUk8GobOLRiwEglNb8nbHuJX0UwJfByYGQxql3SYAx1mlvdd0BdMV9y2uV4anaUy6-rKh0YVPudWC179ryz1YJwzHDn0tWndRKyDmm_4QYlbI0CLKWzjNB5EZFZDRprGYR7PzbMzFrUcRa6eI_df0ZT6Enrxm6FHQd6fuzFGwQmcWN-XhAqAEfLqKZF-CmKAIPYoNE9yXsm5OGw0P1K3Mh9OLrmGi35T1OfyZy4hu-uD9BRtP4DhCJZQIU4i3F_wQF7uaOEzXtnBulo78DdPioPUe7DJnsHdaQ6EeK5c050Ovb5xwKT5YQ'
# director@casting.com Director123
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilc5bTVEM3FEQ1Etc3BUcWFlVldPeiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2FzdGluZy1hZ2VuY3kuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzU5ZThkOTQ2NzEyMDA2NzVjYWVjMyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTk3NDkwMDE1LCJleHAiOjE1OTc0OTcyMTUsImF6cCI6IkxDN1NYSDNzMVpSekkwYkFIelduaFNZRk9hZ1hONnllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.bc-2pj-S5EofwPAZXezMcHKnyhFdFqZA3spAu-zWurLOXk8kaM3ZfmH_kUiw045yvc-QpfuaF_IsDgVdqpHkwEhMiKZBzdQ31apJIiGKmnAvoSzOKy3EnjwzO9OojJAfPfoKbC9RrAKBg8OhTAW_b23pefuoO6FDTO6VuSZy_8mbDb_iOgViJzCd4dFDPyRWPXymRiUyZ6TfRdNdYKVkJN_K6EyzOhkQLe-vElPN1abYuTQLFmpmniNLxoyEF8p3hnbZahquy69cn047x0yXk21u7t_IVEbR63pw4rhaDx7LWl0xyQTkb2r_T14MV-pheXvfu7PEbMJOE8rj7N3e4Q'
# producer@casting.com Producer123
producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilc5bTVEM3FEQ1Etc3BUcWFlVldPeiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2FzdGluZy1hZ2VuY3kuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzU5ZWQyNGVlNTAzMDA2ZDY2YzI5MyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTk3NDg5OTY4LCJleHAiOjE1OTc0OTcxNjgsImF6cCI6IkxDN1NYSDNzMVpSekkwYkFIelduaFNZRk9hZ1hONnllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.tKU39RZiXQMaEoT5rp6KXXoB4aAeLvZWAX1wyCH-Wm9Z8K-XxZHOJIfPFh-dFTXUUc4fes0Ak6wJGbqgXEh_PZPRS2nml9NVRsQfsCNPyDBM5QNtwYhGYwPY-U0E8RkUXDyX464UhkjkhtsXOtpWzckRrjqKOMNtHcVHRvCFWL-kSBjOwx9b7p0rJ7pqq9ISENOYX4sJ3omaEbrn62TCLf-czQuTwYZ9pNuODdZi9TV0mKEGEZxdBKQrET4i-Fb6uV3iQcNv5v0_nTAYOzFx2Xkgtiyiv22ITLNq9dc2JQoHwpGzBK7UOgIlINB4t_a4bxgTZthkO8vBZnreqtGwlw'
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
        self.database_name = "d8qvbansrhno7g.db"
        self.database_path = 'postgres://swxayeqfonggry:338e4eb17b6dd460381b43cbfa8a38c0069fb2859a6f84f59c2cdb8e0e193fc7@ec2-34-204-22-76.compute-1.amazonaws.com:5432/d8qvbansrhno7g'
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
        self.assertEqual(data['deleted'], actor_id)

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
        self.assertEqual(data['deleted'], actor_id)

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
