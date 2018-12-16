from flask import Flask, render_template, request, jsonify
from data.questions import Questions as quiz

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1> Delete Question </h1>"


@app.route('/question/<string:q_id>', methods=['DELETE'])
def del_question(q_id):
    for q_inx, question in enumerate(quiz):
        if question['id'] == q_id or question['id'][2:] == q_id:
            quiz.pop(q_inx)
            return jsonify({"Question Deleted succesfully": quiz})

    return jsonify({"Question index invalid": "Question not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
