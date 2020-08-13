
import os
from flask import Flask, request, jsonify, abort, render_template
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Actor, Movie

import json
from flask_cors import CORS

app = Flask(__name__)
setup_db(app)
CORS(app)



## ROUTES

@app.route('/')
def index():
    return render_template('index.html')

'''
ENDPOINT
    GET /actors
        - public endpoint
        - Expected to return status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
        or appropriate status code indicating reason for failure
'''

@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors():
    try:
        actors = Actor.query.order_by(Actor.id).all()

        return jsonify({
            'success': True,
            'actors': [actor.short() for actor in actors]
        }), 200
    except:
        abort(404)

'''
ENDPOINT
    GET /movies
        - public endpoint
        - Expected to return status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
        or appropriate status code indicating reason for failure
'''

@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies():
    try:
        movies = Movie.query.order_by(Movie.id).all()

        return jsonify({
            'success': True,
            'movies': [movie.short() for movie in movies]
        }), 200
    except:
        abort(404)


'''
ENDPOINT
    POST /actors
        - Create a new row in the actors table
        - Requires the 'post:actors' permission
        - Expected to return status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor
        or appropriate status code indicating reason for failure
'''

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_drink(payload):

    data = request.get_json()
    if 'name' and 'age' and 'gender' not in data:
        abort(422)

    name = data['name']
    age = data['age']
    gender = data['gender']

    actor = Actor(name=name, age=age, gender=gender)

    actor.insert()

    return jsonify({
        'success': True,
        'actors': [actor.long()]
    })

'''
ENDPOINT
    POST /movies
        - Create a new row in the movies table
        - Requires the 'post:movies' permission
        - Expected to return status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie
        or appropriate status code indicating reason for failure
'''

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(payload):

    data = request.get_json()
    if 'title' and 'release_date' not in data:
        abort(422)

    title = data['title']
    release_date = data['release_date']

    movie = Movie(title=title, release_date=release_date)

    movie.insert()

    return jsonify({
        'success': True,
        'movies': [movie.long()]
    })

'''
ENDPOINT
    PATCH /actors/<id>
        where <id> is the existing model id
        - Edits actor
        - Requires the 'patch:actors' permission
        - Expected to return status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
        - Expected to respond with a 404 error if <id> is not found
'''

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, id):

    actor = Actor.query.get(id)
    if actor is None:
        abort(404)

    data = request.get_json()
    if 'title' in data:
        actor.name = data['name']

    if 'age' in data:
        actor.age = data['age']

    if 'gender' in data:
        actor.gender = data['gender']

    actor.update()

    return jsonify({
        'success': True,
        'actors': [actor.long()]
    })

'''
ENDPOINT
    PATCH /movies/<id>
        where <id> is the existing model id
        - Edits movie
        - Requires the 'patch:drinks' permission
        - Expected to return status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
        - Expected to respond with a 404 error if <id> is not found
'''

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, id):

    movie = Movie.query.get(id)
    if movie is None:
        abort(404)

    data = request.get_json()
    if 'title' in data:
        movie.title = data['title']

    if 'release_date' in data:
        movie.release_date = data['release_date']


    movie.update()

    return jsonify({
        'success': True,
        'movies': [movie.long()]
    })



'''
ENDPOINT
    DELETE /actors/<id>
        where <id> is the existing model id
        - Deletes actor
        - Require the 'delete:actors' permission
        - Expected to return status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
        - Expected to respond with a 404 error if <id> is not found
'''

@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, id):

    actor = Actor.query.get(id)
    if actor is None:
        abort(404)

    actor.delete()

    return jsonify({
        'success': True,
        'delete': actor.id
    })

'''
ENDPOINT
    DELETE /movies/<id>
        where <id> is the existing model id
        - Deletes movie
        - Require the 'delete:movies' permission
        - Expected to return status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
        - Expected to respond with a 404 error if <id> is not found
'''

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, id):

    movie = Movie.query.get(id)
    if movie is None:
        abort(404)

    movie.delete()

    return jsonify({
        'success': True,
        'delete': movie.id
    })



## Error Handling

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }),400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }),404

@app.errorhandler(405)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }),405

@app.errorhandler(422)
def uproccessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unproccessable'
    }),422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }),500

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code




if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)