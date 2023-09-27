# router.py
from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_limiter.util import get_remote_address
from .app import fetch_secret
import logging
import os

# Initialize secrets
API_TOKEN = os.environ['API_TOKEN']
FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']
CODE_NAME = os.environ['CODE_NAME']

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "fallbackSecretKey")
s = Serializer(app.config["SECRET_KEY"])
logging.basicConfig(
    level=logging.INFO,
    filename="audit.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per minute", "5 per second"],
)


@app.route("/health", methods=["GET"])
@limiter.limit("5 per minute")
def health_check():
    logging.info("Health check requested.")
    return jsonify(
        {
            "status": "healthy",
            "container": os.environ.get("CONTAINER_REGISTRY", "unknown"),
        }
    )


@app.route("/token", methods=["GET"])  # Generate a token
def get_token():
    token = s.dumps({"token": API_TOKEN})
    return jsonify(token=token)

@app.route("/secret", methods=["GET"])
@limiter.limit("5 per second")
def get_secret():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        logging.warning("Missing Authorization header.")
        abort(403, description="Missing Authorization header")

    auth_parts = auth_header.split(" ")
    if len(auth_parts) != 2 or auth_parts[0] != "Bearer" or auth_parts[1] != API_TOKEN:
        logging.warning("Invalid API token.")
        abort(403, description="Invalid API token")

    # Fetch both secret and codeName from DynamoDB
    secret_code, codeName_from_db = fetch_secret(CODE_NAME)

    if CODE_NAME != codeName_from_db:
        logging.warning(f"Invalid codeName attempt: Expected {CODE_NAME}, got {codeName_from_db}")
        abort(403, description="Invalid codeName.")

    if secret_code:
        return jsonify({"codeName": codeName_from_db, "secretCode": secret_code})
    else:
        abort(404, description="Secret code not found.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)