from flask import Flask, render_template, request, jsonify
from data.questions import Questions as quiz
from data.answers import Answers as ans
from data.userdata import Users as users

app = Flask(__name__)


@app.route('/question/<string:q_id>/answer', methods=['POST'])
def add_answer_to_question(q_id):
    for question in quiz:
        if question["id"] == q_id or question["id"][2:] == q_id:
            #  question found
            question_ans = request.get_json()

            for user in users:
                if user["username"] == question_ans["answer-username"]:
                  #  user exists
                    return jsonify({"Answer added successfully": [{"Question": question["description"]}, {"Added Answer": question_ans["answer-desc"]}]}), 201

            return jsonify({"Invalid username": "User not found thus can't answer question"}), 403

    return jsonify({"Question id not found": "Question does not exist"}), 404


if __name__ == "__main__":
    app.run(debug=True)
