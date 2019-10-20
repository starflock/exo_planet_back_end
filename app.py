# Required Imports
import os

from build_google_creds import build_creds
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from sentry_sdk import init
from flask_cors import CORS

sentry_dsn = os.environ.get("SENTRY_DSN")
# Initialize Sentry
init(sentry_dsn)

# Build Environmental Variables
# run heroku config -s >> .env on your local machine
# run gunicorn app:app test_mode
build_creds()

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('creds/starflock-exo-planet-firebase-key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_planet_config_table = db.collection('users_planet_configurations')


# https://exo-planet-starflock-backend.herokuapp.com/
@app.route('/', methods=['GET'])
def home():
    """
        Landing Page
    """
    return jsonify({"Details": "Go to https://github.com/starflock/exo_planet_back_end"})


@app.route('/create_user', methods=['POST'])
def create_user():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        username = request.json['username']
        if not username:
            return jsonify({"Error": "username is required."}, 400)
        user = get_user_from_db(username)
        if user:
            return jsonify({"Error": "username is taken."}, 403)
        user_planet_config_table.document(username).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


def update_user_db(username, request):
    user_planet_config_table.document(username).update(request.json)


def get_user_from_db_by_username_and_password(username, password):
    user = user_planet_config_table.document(username).get()
    if user.get("password") == password:
        return False
    return user.to_dict()


@app.route('/update_user', methods=['POST', 'PUT'])
def update_user():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        username = request.json['username']
        password = request.json['password']
        if not username:
            return jsonify({"Error": "username is required."}, 400)
        if not password:
            return jsonify({"Error": "password is required."}, 400)

        user = get_user_from_db_by_username_and_password(username, password)
        if not user:
            return jsonify({"Error": "Invalid Creds."}, 400)
        update_user_db(username, request)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


def get_user_from_db(username):
    user = user_planet_config_table.document(username).get()
    return user.to_dict()


@app.route('/get_user', methods=['GET'])
def get_user():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        username = request.args.get('username')
        if username:
            user = get_user_from_db(username)
            if user:
                return jsonify(user), 200
            else:
                return jsonify({"Error": "User does not exist."}, 400)

        return jsonify({"Error": "username is required."}, 400)
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        all_users = [doc.to_dict() for doc in user_planet_config_table.stream()]
        return jsonify(all_users), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        username = request.json['username']
        if not username:
            return jsonify({"Error": "username is required."}, 400)
        user_planet_config_table.document(username).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/ishabitable', methods=['GET'])
def ishabitable():
    orb_dist = float(request.args.to_dict().get('orbital_distance'))
    solar_mass = float(request.args.to_dict().get('solar_mass'))

    t_min = 149600000000
    t_max = 1989000000000000000000000000000

    r_orb = orb_dist * t_min

    l_slmass = solar_mass * (t_max**4)

    s = 0.0000000567

    t1 = 5554571841 * (t_min)
    t2 = 19356878641 * (t_max)

    val_1 = l_slmass / ((4) * (3.14) * (t1) * (s))
    r_orb_1 = val_1 ** 0.5

    val_2 = l_slmass / ((4) * (3.14) * (t2) * (s))
    r_orb_2 = val_2 ** 0.5
    if r_orb < r_orb_2 and r_orb > r_orb_1:
        return jsonify({"ishabitable": True}), 200

    return jsonify({"ishabitable": False}), 200


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
