import requests
import os
from dotenv import load_dotenv

get_url = "http://localhost:8080/api/course/details"
load_dotenv(".env")

headers = {"Authorization": f"Bearer {os.getenv('SERVICE_JWT')}"}

print(headers)

response = requests.get(get_url, headers=headers)

print(response.json())

post_url = "http://localhost:8080/api/course/recommendations"

response = requests.post(post_url, json="data/test.json")

# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
# @app.route('/api/receive-course', methods=['POST'])
# def receive_course():
#     course_data = request.get_json()
#     print(course_data)
#     return jsonify({"message": "Course received successfully", "course": course_data}), 200
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)