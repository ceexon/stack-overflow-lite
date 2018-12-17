from flask import Flask, request, jsonify, render_template
from data.answers import Answers as ans
from data.questions import Questions as quiz
from data.userdata import Users as user

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>It works</h1>"


@app.route('/question', methods=['GET'])
def det_all_questions():
    asked = []
    for i, question in enumerate(quiz):
        numi = str(i+1)
        asked.append({numi+'. ': question["description"]})

    if asked == []:
        return "No questions found", 404

    return jsonify({"All questions": asked})


if __name__ == "__main__":
    app.run(debug=True)
