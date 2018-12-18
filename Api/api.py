from flask import Flask, request, jsonify
from data.userdata import Users as users

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>User sign up</h1>"


@app.route("/auth/signup", methods=["POST"])
def signup():
    user_data = request.get_json()
    for user in users:
        if user_data["username"] == user["username"]:
            return jsonify("Usename already exists")
        if user_data["email"] == user["email"]:
            return jsonify("Email already exists")

    users.append(user_data)
    return jsonify("User added successfully"), 201


app.run()
