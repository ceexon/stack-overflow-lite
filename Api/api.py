from flask import Flask, render_template, request, jsonify
from data.questions import Questions as quiz
from data.userdata import Users as users

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>User can get a question</h1>"

# Get question by username


@app.route('/question/user/<string:name>', methods=['GET'])
def get_quiz_by_username(name):
    user_name = ''
    for user in users:
        if user["username"] == name:
            user_name = name
    if user_name == '':
        return jsonify({404: "User not found so no related questions"}), 404
    else:
        asked = []
        ct = 1
        for question in quiz:
            if question["asker-username"] == user_name:
                asked.append({str(ct)+'. ': question['description']})
                ct += 1
        if asked == []:
            return jsonify({'Questions by ' + user_name: "User has not asked any questions"}), 404

        else:
            return jsonify({'Questions by ' + user_name: asked}), 200


# Get question by category
@app.route('/question/category/<string:cat>', methods=['GET'])
def get_quiz_by_category(cat):
    available_categories = []
    asked = []

    # creating a list of existing categories
    for question in quiz:
        for a_cat in question["category"]:
            if a_cat in available_categories:
                pass
            else:
                available_categories.append(a_cat)

    # check if user posted category is in avalable category
    if cat in available_categories:
        cat_quiz_count = 1
        for question in quiz:
            if cat in question["category"]:
                asked.append(
                    {str(cat_quiz_count) + '. ': question['description']})
                cat_quiz_count += 1

        return jsonify({"Questions in " + cat + " category": asked}), 200

    else:
        return jsonify({404: "Category not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
