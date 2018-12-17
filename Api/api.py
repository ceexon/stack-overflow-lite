from flask import Flask, render_template, request, jsonify
from data.answers import Answers as ans
from data.questions import Questions as quiz
from data.userdata import Users as users

app = Flask(__name__)


@app.route('/question/<string:q_id>/answer/<string:a_id>', methods=['PUT'])
def acceptUpdate_ans(q_id, a_id):
    input_ans = request.get_json()
    input_ans["questin-id"] = q_id
    input_ans["answer-id"] = a_id
    username = ""
    question_exists = ""
    answer_exists = ""
    ask_or_ans = ""
    the_question = {}
    the_answer = {}

    # verify user by username
    for user in users:
        if user["username"] == input_ans["username"]:
            username = input_ans["username"]

    if username == "":
        return jsonify({"User not found": "Invalid username"}), 404

    # verify question by question id
    for question in quiz:
        if q_id == question["id"]:
            question_exists = question["id"]
            for key in question:
                the_question[key] = question[key]

    if question_exists == "":
        return jsonify({"Question not found": "invalid question id"}), 404

    # verify answer by answer id
    for answer in ans:
        if a_id == answer["answer-id"]:
            answer_exists = answer["answer-id"]
            for key in answer:
                the_answer[key] = answer[key]
            # check if its the right question and answer pair by both ids
            if q_id != answer["questin-id"]:
                return jsonify({"Mismatched pair": "Answer is not for specified question"})

            if username == answer["answer-username"]:
                ask_or_ans = "ans"
            elif username == the_question["asker-username"]:
                ask_or_ans = "ask"
            else:
                return jsonify({"Unauthorized user": "You cannot accept or update an answer you did not write and can't accept or reject an answer to a question you did not ask"}), 401

    if answer_exists == "":
        return jsonify({"Answers not found": "invalid answer id"}), 404

    if ask_or_ans == "ans":
        # can only update answer
        ans_desc = input_ans["answer-desc"]
        if ans_desc == the_answer["answer-desc"]:
            return jsonify({"User viewed the answer": "Did not update it"}), 200
        the_answer["answer-desc"] = ans_desc
        for key in input_ans:
            if key != "answer-desc" and key != "username":
                if the_answer[key] != input_ans[key]:
                    return jsonify({"Permision Denied": "You do not have privilege to make such changes on " + key}), 403

        return jsonify({"Answer updated successfully": [{"Question ": the_question}, {"Answer": the_answer}]}), 201
    else:
        acc_ans = input_ans["accepted"]
        the_answer["accepted"] = input_ans["accepted"]
        for key in input_ans:
            if key != "accepted" and key != "username":
                if the_answer[key] != input_ans[key]:
                    return jsonify({"Permision Denied": "You do not have privilege to make such changes on " + key}), 403

        if the_answer["accepted"] == "true":
            return jsonify({"Answer Has been accepted": the_answer}), 201
        elif the_answer["accepted"] == "false":
            return jsonify({"Answer Has been rejected": the_answer}), 201
        else:
            return jsonify({"User viewed the answer": "Not yet accepted or rejected"}), 200


if __name__ == "__main__":
    app.run(debug=True)
