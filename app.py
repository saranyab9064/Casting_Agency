
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from auth import AuthError, requires_auth
from flask_cors import CORS
from models import setup_db,Movie,Actor,db
from auth import API_AUDIENCE, AUTH0_CALLBACK_URL, AUTH0_CLIENT_ID

AUTH0_DOMAIN = 'proj03.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting-agency'
AUTH0_CLIENT_ID = "070qQHnIb8nGTLxS1M5eXTwpTJUEdbi3"
AUTH0_CALLBACK_URL = "http://localhost:8100"


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # Reference from the Udacity lesson "flask-cors"
    #   CORS(app)
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
       response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
       response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
       return response

    @app.route('/authorization/url',methods=['GET'])
    def generate_auth_url():
        url = f'https://{AUTH0_DOMAIN}/authorize' \
              f'?audience={API_AUDIENCE}' \
              f'&response_type=token&client_id=' \
              f'{AUTH0_CLIENT_ID}&redirect_uri=' \
              f'{AUTH0_CALLBACK_URL}'

        return jsonify({
            'auth_url': url
        })

    # Default End Points
    @app.route('/')
    def home_page():
        print("am with default")
        return 'Welcome to the Capstone Casting Agency Project'


    # API Route - Movie
    @app.route('/movies', methods=['GET'])
    def get_to_list_movies():
        """
        Query all movies list
        """
        movies_list = Movie.query.all()
        print(movies_list)
        response = {
            'success': True,
            'status_code': 200,
            'movies': [i.format() for i in movies_list]
        }
        print("am here")
        result = jsonify(response)
        return result


    @app.route('/movies/<movie_id>', methods=['GET'])
    @requires_auth('get:movies/<movie_id>')
    def filter_movie_by_id(data, movie_id):
        """
        Filter movie based on  id
        """
        movies_list = Movie.query.get(movie_id)
        if movies_list is None:
            abort(404)
        else:
            response = {
                'movies': movies_list.format(),
                'success': True,
                'status_code': 200
            }
            result = jsonify(response)
            return result


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(data):
        """
        Add movie to the list
        """
        movie_title = request.get_json().get('movie_title', None)
        movie_release_date = request.get_json().get('movie_release_date', None)
        if movie_title is None or movie_release_date is None:
            abort(404)
        else:
            movies_list = Movie(movie_title=movie_title, movie_release_date=movie_release_date)
            try:
                movies_list.insert()
                response = {
                    'movies': movies_list.format(),
                    'success': True,
                    'status_code': 200
                }
                result = jsonify(response)
                return result
            except Exception as message:
                print(message)
                abort(500)


    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies/<movie_id>')
    def update_movie(data, movie_id):
        """
        Post movie to the list
        """
        movie_title = request.get_json().get('movie_title', None)
        movie_release_date = request.get_json().get('movie_release_date', None)

        movies_list = Movie.query.get(movie_id)
        if movie_title is None or movie_release_date is None or movies_list is None:
            abort(404)
        else:
            movies_list.movie_title = movie_title
            movies_list.movie_release_date = movie_release_date
        try:
            movies_list.update()
            response = {
                'movies': movies_list.format(),
                'success': True,
                'status_code': 200
            }
            result = jsonify(response)
            return result
        except Exception as message:
            print(message)
            abort(500)


    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies/<movie_id>')
    def movie_del(data, movie_id):
        """
        Delete movie from the movie list
        """
        del_movie = Movie.query.get(movie_id)
        if del_movie is None:
            abort(422)
        else:
            try:
                del_movie.delete()
                response = {
                    'success': True,
                    'status_code': 200
                }
                result = jsonify(response)
                return result
            except Exception as message:
                print(message)
                abort(500)


    # Route - Actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_to_list_actors(data):
        """
        Query to fetch all actors list
        """
        actors_list = Actor.query.all()
        response = {
            'success': True,
            'status_code': 200,
            'movies': [i.format() for i in actors_list]
        }
        result = jsonify(response)
        return result


    @app.route('/actors/<actor_id>', methods=['GET'])
    @requires_auth('get:actors/<actor_id>')
    def filter_actor_by_id(data, actor_id):
        """
        Filter actor based on id
        """
        actors_list = Movie.query.get(actor_id)
        if actors_list is None:
            abort(404)
        else:
            response = {
                'movies': actors_list.format(),
                'success': True,
                'status_code': 200
            }
            result = jsonify(response)
            return result


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(data):
        """
        Add actor to the list
        """
        actor_name = request.get_json().get('actor_name', None)
        actor_age = request.get_json().get('actor_age', None)
        actor_gender = request.get_json().get('actor_gender', None)
        new_actor = Actor(actor_age=actor_age,
                          actor_name=actor_name,
                          actor_gender=actor_gender)
        if actor_name is None or actor_age is None or actor_gender is None:
            abort(404)
        else:
            try:
                new_actor.insert()
                response = {
                    'movies': new_actor.format(),
                    'success': True,
                    'status_code': 200
                }
                result = jsonify(response)
                return result
            except Exception as message:
                print(message)
                abort(500)


    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors/<actor_id>')
    def update_actors(data, actor_id):
        """
        Update actor to the list
        """
        actor_name = request.get_json().get('actor_name', None)
        actor_age = request.get_json().get('actor_age', None)
        actor_gender = request.get_json().get('actor_gender', None)
        new_actor = Actor.query.get(actor_id)
        if actor_name is None or actor_age is None or actor_gender is None:
            abort(404)
        else:
            new_actor.actor_age = actor_age
            new_actor.actor_name = actor_name
            new_actor.actor_gender = actor_gender
            try:
                new_actor.update()
                response = {
                    'movies': new_actor.format(),
                    'success': True,
                    'status_code': 200
                }
                result = jsonify(response)
                return result
            except Exception as message:
                print(message)
                abort(500)


    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors/<actor_id>')
    def actor_del(data, actor_id):
        """
        Delete actor from the actors list
        """
        del_actor = Actor.query.get(actor_id)
        if del_actor is None:
            abort(422)
        else:
            try:
                del_actor.delete()
                response = {
                    'success': True,
                    'status_code': 200
                }
                result = jsonify(response)
                return result
            except Exception as message:
                print(message)
                abort(500)


    # Error Handling

    '''
    Example error handling for unprocessable entity
    '''


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    '''
    Error handler for Page not found or Server not found
    '''


    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Page not found or Server not found"
        }), 404


    '''
    Error handler for Unauthorized client status
    '''


    @app.errorhandler(401)
    def Unauthorized_client(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized client status"
        }), 401


    '''
    Error handler for Bad Request from client to server
    '''


    @app.errorhandler(400)
    def bad_request_to_server(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request from client to server"
        }), 400


    '''
    Error handler for Internal Server Error server or Bad Gateway
    '''


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error server or Bad Gateway"
        }), 500


    '''
    @TODO implement error handler for AuthError
    '''


    @app.errorhandler(AuthError)
    def auth_error(error_msg):
        return jsonify({
            "success": False,
            "error": error_msg.status_code,
            "message": error_msg.error['description']
        }), error_msg.status_code
    return app
APP = create_app()

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
# Default port:
if __name__ == '__main__':
    APP.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
