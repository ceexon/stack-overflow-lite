from flask import Flask, render_template, request, jsonify
from data.questions import Questions as quiz
from data.answers import Answers as ans

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
