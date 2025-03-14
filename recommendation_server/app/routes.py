from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import requests
from recommendation_server.app.recommender import generate_recommendations
from recommendation_server.app.config import JAVA_CALLBACK_URL
from recommendation_server.app.vectorizer import vectorize_courses
import os

load_dotenv(".env")

api_blueprint = Blueprint('api', __name__)
headers = {"Authorization": f"Bearer {os.getenv('SERVICE_JWT')}"}


@api_blueprint.route('/recommend', methods=['POST'])
def recommend():

    try:
        courses = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 400

    result = generate_recommendations(courses)

    try:
        callback_response = requests.post(JAVA_CALLBACK_URL, json=result, headers=headers)
        callback_response.raise_for_status()
    except Exception as e:
        return jsonify({"error": "Failed to call Java callback", "message": str(e)}), 500

    return jsonify({
        "status": "success",
        "message": "Recommendations sent to Java",
        "javaResponse": callback_response.text
    }), 200


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