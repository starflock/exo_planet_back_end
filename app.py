# Required Imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB
cred = credentials.Certificate('starflock-exo-planet-firebase-key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_planet_config_table = db.collection('users_planet_configurations')
# import pdb; pdb.set_trace()


@app.route('/', methods=['GET'])
def home():
    """
        Landing Page
    """
    return jsonify({"Details": "Go to https://github.com/starflock/exo-plan-it"})


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
            update_user_db(username, request)
            return jsonify({"success": True}), 200
        user_planet_config_table.document(username).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


def update_user_db(username, request):
    user_planet_config_table.document(username).update(request.json)


@app.route('/update_user', methods=['POST', 'PUT'])
def update_user():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        username = request.json['username']
        if not username:
            return jsonify({"Error": "username is required."}, 400)
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


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
