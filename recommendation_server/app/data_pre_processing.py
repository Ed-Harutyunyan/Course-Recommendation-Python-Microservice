import os
import re
import json

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

OUTPUT_FILE = "data/processed_courses.json"

def preprocess_text(text: str) -> str:

    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces

    tokens = word_tokenize(text)
    processed_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]

    return " ".join(processed_tokens)


def process_courses(courses):
    """Processes a list of JSON objects, extracts and preprocesses course descriptions."""
    processed_courses = []

    for course in courses:
        if "courseDescription" in course :
            processed_text = preprocess_text(course["courseDescription"])
            course["courseDescription"] = processed_text  # Add new field with processed description
            processed_courses.append(course)

    return processed_courses


def save_processed_courses(courses):
    """Processes the courses and saves the results in a JSON file."""
    processed_courses = process_courses(courses)

    # Ensure 'data' directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_courses, f, indent=4, ensure_ascii=False)

    print(f"Processed courses saved to {OUTPUT_FILE}")

