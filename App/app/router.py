from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import App.app.secret_handler as secret_handler  # your secret handler
import logging
import os
import jwt
import datetime

# Initialize secrets
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'testsecret')
CODE_NAME = os.environ.get('CODE_NAME', 'default_value')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'test_api')

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

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

# Function to verify JWT token
def verify_jwt_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    return payload

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

@app.route("/token", methods=["GET"])
def get_token():
    token = jwt.encode({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, JWT_SECRET_KEY, algorithm="HS256")
    return jsonify(token=token)

@app.route("/secret", methods=["GET"])
@limiter.limit("5 per second")
def get_secret():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        logging.warning("Missing Authorization header.")
        abort(403, description="Missing Authorization header")

    auth_parts = auth_header.split(" ")
    if len(auth_parts) != 2 or auth_parts[0] != "Bearer":
        logging.warning("Invalid API token.")
        abort(403, description="Invalid API token")

    try:
        verify_jwt_token(auth_parts[1])
    except jwt.ExpiredSignatureError:
        logging.warning("Token has expired.")
        abort(403, description="Token has expired")
    except jwt.InvalidTokenError:
        logging.warning("Invalid token.")
        abort(403, description="Invalid token")

    # Fetch both secret and codeName from DynamoDB
    secret_code, codeName_from_db = secret_handler.fetch_secret(CODE_NAME)

    if CODE_NAME != codeName_from_db:
        logging.warning(f"Invalid codeName attempt: Expected {CODE_NAME}, got {codeName_from_db}")
        abort(403, description="Invalid codeName.")

    if secret_code:
        return jsonify({"codeName": codeName_from_db, "secretCode": secret_code})
    else:
        abort(404, description="Secret code not found.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
