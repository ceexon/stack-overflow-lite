from flask import Flask, render_template, request, jsonify
from data.questions import Questions as quiz
from data.userdata import Users as users

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Post a question</h1>"


@app.route('/user/ask_question', methods=['POST'])
def add_question():
    global quiz
    quiz_data = request.get_json()
    create_quiz = {}
    for key in quiz_data:
        create_quiz[key] = quiz_data[key]

    for user in users:
        if user["username"] == create_quiz["asker-username"]:
            for question in quiz:
                if create_quiz["description"] == question["description"]:
                    return jsonify({"Question already exists": question})
            quiz.append(create_quiz)
            return jsonify({"Question added succesfully(end of list)": quiz}), 201

    return jsonify({"username not found": "User does not exist. Create an account to be able to post questions"}), 404


if __name__ == "__main__":
    app.run(debug=True)
