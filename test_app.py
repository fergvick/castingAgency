import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from datetime import datetime

# assistant@casting.com Assistant123
assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilc5bTVEM3FEQ1Etc3BUcWFlVldPeiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2FzdGluZy1hZ2VuY3kuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzU5ZGQ4MTcwNGFmMDA2ZGRmMjhjMSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTk3NDMyNTE4LCJleHAiOjE1OTc0Mzk3MTgsImF6cCI6IkxDN1NYSDNzMVpSekkwYkFIelduaFNZRk9hZ1hONnllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.icZojHH1IdbWabkxasl3No5ZsQaGFz_AbQsIg28ufqsx9jctLTIgCz_eDlQagfrBTyJynvZ9Bwt3T0VqqU3m8r9FAe7QHyla0ddlJJ0mJMRdlbt_hE2Kz_Ixf5gsirmiDrrzJd8hWOQkHK-R2bpHHYdWq6xBkW3I96Vl2tE-lH8Zxa2c17BxevHoIFKjFFbHP1yw9m5lsL8RF2_V-mGUIKcBT_W401kG71v7p9WTC9gZEGrjBUmh1JBJdNzZuwO8FeNqCldMyotj_SLGH4EFIna8asNUgN7i3fpIfmHGYxhx6rDU__ukicHwq024utx5Znh97N__K2HbCIYOWSI3zA'

# director@casting.com Director123
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilc5bTVEM3FEQ1Etc3BUcWFlVldPeiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2FzdGluZy1hZ2VuY3kuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzU5ZThkOTQ2NzEyMDA2NzVjYWVjMyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTk3NDMyNDU2LCJleHAiOjE1OTc0Mzk2NTYsImF6cCI6IkxDN1NYSDNzMVpSekkwYkFIelduaFNZRk9hZ1hONnllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.HbXTMXBzxaazPslsb1KHq5GZQLblGLlYMB-mqW66UgbT3DyJ1Jv989B9qvCITEM1UBfGrSAvjEuFxrCLofdlSEg6e1pH54OcAIID8VmaepStDNBdTQ8P85q2g0l8IqaRAQIEYbACGzwNWJ0QtxunMFNm7j5VmiMGxTz0oVgtwsfT-1rY2rZqKgF6YfOv9tR2RVpQXtXcxTDSzqLmPvXLM8OQMjYueSyUqs6DVSrfUlRiOwOBmdAVGJtwi9-f15CXxZKmW3lH4ow4hsneVOLIjgd9ilpZL6pJOGouFmHB4MhSkieYOwxLujOjjscdCT53dz3Jto7GI4te8GYFJABybQ'

# producer@casting.com Producer123
producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilc5bTVEM3FEQ1Etc3BUcWFlVldPeiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY2FzdGluZy1hZ2VuY3kuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzU5ZWQyNGVlNTAzMDA2ZDY2YzI5MyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTk3NDMyMzQ4LCJleHAiOjE1OTc0Mzk1NDgsImF6cCI6IkxDN1NYSDNzMVpSekkwYkFIelduaFNZRk9hZ1hONnllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.T3s6zXpbGMK02lGLOqo8QgRPywIpXXuHMz1gSAw8ZzQk0XwiYiEx3IEg5p7o1naxVcTxxmic8HWRsAWBetZmkOyh71zTDeaRJA6LU5-XosC7TfWzRNyfE9SIfT_YrT9O-A814XRI8S9DFSyJ7nL0jlUhmTtZDhhl9DS3BLvddxqkcfx0YoDtS7KOdTdFWdY2U4jt_-gF9Yrcm1iwk3F4bR8GjPmBL2tDshmDTsIqXR_TWeHpih3DGJZiKDV1tumiAA7K9FMI3VsneM0faSTzhYu2YNth2qMfEZEDGeXeewZAmU1kkJLtTT0W3fCFCIehrKYiJJZhtsV_TAqnHJRzig'

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
        self.database_name = "test.db"
        self.database_path = 'postgres://snkljcpdwalgvg:09268410a1f491cfeac7ec6150a5c7cafd10f11bceee4f751161aebe883d68d5@ec2-184-72-162-198.compute-1.amazonaws.com:5432/'+self.database_name
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
