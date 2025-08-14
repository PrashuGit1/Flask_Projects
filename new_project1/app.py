from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Replace with strong secret in real use

jwt = JWTManager(app)

# Dummy user database
users = {
    "prakash": "password123",
    "admin": "adminpass"
}

@app.route('/')
def home():
    return jsonify(message="Welcome to the API! Use /login to get a token.")

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    return jsonify(message="Invalid credentials"), 401

# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello {current_user}, you have access to protected data!")

if __name__ == '__main__':
    app.run(debug=True)
