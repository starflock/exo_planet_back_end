import os
import json

google_creds = {
    "type": os.environ.get("GOOGLE_FIREBASE_TYPE"),
    "project_id": os.environ.get("GOOGLE_FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("GOOGLE_FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("GOOGLE_FIREBASE_PRIVATE_KEY"),
    "client_email": os.environ.get("GOOGLE_FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("GOOGLE_FIREBASE_CLIENT_ID"),
    "auth_uri": os.environ.get("GOOGLE_FIREBASE_AUTH_URI"),
    "token_uri": os.environ.get("GOOGLE_FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("GOOGLE_FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.environ.get("GOOGLE_FIREBASE_CLIENT_CERT_URL")
}


def build_creds():
    filename = "creds/starflock-exo-planet-firebase-key.json"
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
        file = open(filename, "w")

        file.write(json.dumps(google_creds))
        file.close()
    else:
        file = open(filename, "w")
        file.write(json.dumps(google_creds))
        file.close()
