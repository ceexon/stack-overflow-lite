from flask import Flask, render_template, request, jsonify
from data.answers import Answers as ans
from data.questions import Questions as quiz
from data.userdata import Users as users

app = Flask(__name__)


@app.route('/question/<string:q_id>/answer/<string:a_id>', methods=['PUT'])
def acceptUpdate_ans(q_id, a_id):
    the_update = request.get_json()
    user_exists = ""
    question_exists = ""
    for question in quiz:
        if q_id == question["id"]:
            question_exists = question["id"]

    if question_exists == "":
        return jsonify("Question not found"), 404
      #  check user existence
    for user in users:
        if user["username"] == the_update["username"]:
         #   check if answer has already been updated before
            answer_exists = ""
            the_old_answer = {}
            for i, answer in enumerate(ans):
                if answer["answer-id"] == the_update["answer-id"]:
                    answer_exists = answer["answer-id"]
                    the_old_answer = answer
                    ans.pop(i)
                    break

            if answer_exists != "":
               #  check if question and answer are rightly matched
                if the_old_answer["questin-id"] == the_update["questin-id"]:
                   # user is one answering
                    if the_old_answer["answer-username"] == the_update["username"]:
                        if the_old_answer["accepted"] != the_update["accepted"]:
                            return jsonify("Sorry!! You can accept or reject your answer"), 401

                        the_old_answer["answer-desc"] = the_update["answer-desc"]
                        return jsonify({"Answer updated successfully": the_old_answer}), 201

                    else:
                        for question in quiz:
                            # user can accept or reject
                            if question["asker-username"] == the_update["username"]:
                                if the_old_answer["answer-desc"] != the_update["answer-desc"]:
                                    return jsonify("Sorry!! You cant update an answer you did not give"), 401
                                the_old_answer["accepted"] = the_update["accepted"]
                                return jsonify({"Answer Accepted": the_old_answer}), 201

                   # wrongly matched questio pair
                return jsonify("Invalid question-answer pair")

         # This is a new answer so it will be added
            if answer_exists == "":
                new_answer = {}
                new_answer["answer-username"] = the_update["username"]
                for key in the_update:
                    if key != "username":
                        new_answer[key] = the_update[key]

                ans.append(new_answer)
                return jsonify({"answer added succesfully": ans}), 201

      # if user does not exist
    if user_exists == "":
        return jsonify("User not found"), 404


if __name__ == "__main__":
    app.run(debug=True)
