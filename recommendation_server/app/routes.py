from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import requests

from recommendation_server.app.recommender import generate_recommendations_by_keywords, generate_recommendations_from_passed_courses
from recommendation_server.app.vectorizer import vectorize_courses
import os

load_dotenv("../../.env")

api_blueprint = Blueprint('api', __name__)
headers = {
    "Authorization": f"Bearer {os.getenv('SERVICE_JWT')}",
    "Content-Type": "application/json"
}


@api_blueprint.route('/recommend/keyword', methods=['POST'])
def recommend_by_keyword():

    try:
        data = request.get_json(force=True)
        keywords = data.get("keywords", [])
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 415

    query_text = ", ".join(keywords)

    return generate_recommendations_by_keywords(query_text, 3)


@api_blueprint.route('/recommend/byPassed', methods=['POST'])
def recommend_by_passed():

    try:
        passed_and_possible_courses = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 415

    passed_ids = passed_and_possible_courses["passed_ids"]
    future_ids = passed_and_possible_courses["possible_ids"]

    return generate_recommendations_from_passed_courses(passed_ids, future_ids, 3)


# # @api_blueprint.route('/send', methods=['GET'])
# def send_recommendations(result):
#     print("JWT Token:", os.getenv("SERVICE_JWT"))
#     print(result)
#     print(headers)
#     # try:
#     #     callback_response = requests.post(JAVA_CALLBACK_URL, json=result, headers=headers)
#     #     # callback_response.raise_for_status()
#     # except Exception as e:
#     #     return jsonify({"error": "Failed to call Java callback", "message": str(e)}), 500
#
#     return result, 200


@api_blueprint.route('/vectorize', methods=['PUT'])
def vectorize():
    try:
        courses = request.get_json(force=True)
        if not courses:
            return jsonify({"error": "JSON empty"}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 400

    vectorize_courses(courses)

    return jsonify({
        "status": "success"
    }), 200


#Testing the connection with dummy data
@api_blueprint.route('/test', methods=['POST'])
def test():
    data = request.get_json(force=True)
    response = {"message": "OK", "data": data}
    return jsonify(response), 200