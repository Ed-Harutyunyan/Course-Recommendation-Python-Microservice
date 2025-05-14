from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, abort

from recommendation_server.app.data_pre_processing import preprocess_text
from recommendation_server.app.recommender import generate_recommendations_by_keywords, \
    generate_recommendations_from_passed_courses, delete_points
from recommendation_server.app.vectorizer import vectorize_courses

load_dotenv("../../.env")

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/recommend/keyword', methods=['POST'])
def recommend_by_keyword():

    try:
        data = request.get_json(force=True)
        keywords = data.get("keywords", [])
        possible_course_ids = data.get("possibleCourseCodes", [])
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 415

    query_text = ", ".join(keywords)

    return generate_recommendations_by_keywords(query_text, possible_course_ids, 5)


@api_blueprint.route('/recommend/message', methods=['POST'])
def recommend_by_message():
    try:
        data = request.get_json(force=True)
        message = data.get("message", "")
        possible_course_ids = data.get("possibleCourseCodes", [])

        if not message:
            return jsonify({"error": "Message is required"}), 400

        processed_text = preprocess_text(message)
        keywords = processed_text.split()

        print(keywords)

        if not keywords:
            return jsonify({"error": "No meaningful keywords found in message"}), 400

        return generate_recommendations_by_keywords(" ".join(keywords), possible_course_ids, 5)

    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 415


@api_blueprint.route('/recommend/byPassed', methods=['POST'])
def recommend_by_passed():

    try:
        passed_and_possible_courses = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 415

    passed_ids = passed_and_possible_courses["passed_course_codes"]
    future_ids = passed_and_possible_courses["possible_course_codes"]

    return generate_recommendations_from_passed_courses(passed_ids, future_ids, 3)


@api_blueprint.route('/vectorize', methods=['PUT'])
def vectorize():
    try:
        courses = request.get_json(force=True)
        print(courses)
        if not courses:
            return jsonify({"error": "JSON empty"}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 400

    vectorize_courses(courses)

    return jsonify({
        "status": "success"
    }), 200

@api_blueprint.route('/delete/points', methods=['DELETE'])
def delete_points_route():
    try:
        delete_points()

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    return jsonify(
        {"status": "success", "message": "All points deleted"}
    ), 200

#Testing the connection with dummy data
@api_blueprint.route('/test', methods=['POST'])
def test():
    data = request.get_json(force=True)
    response = {"message": "OK", "data": data}
    return jsonify(response), 200