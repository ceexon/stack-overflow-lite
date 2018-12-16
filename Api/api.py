from flask import Flask, render_template, request, jsonify
from data.answers import Answers as ans
from data.questions import Questions as quiz
from data.userdata import Users as users

app = Flask(__name__)


@app.route('/question/<string:q_id>/answer/<string:a_id>', methods=['PUT'])
def update_accept_ans():
    pass


if __name__ == "__main__":
    app.run(debug=True)
