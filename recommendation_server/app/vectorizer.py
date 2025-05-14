import hashlib

from recommendation_server.app.config import qdrant_client, openai_client, collection_name, OUTPUT_FILE, AI_model
from recommendation_server.app.data_pre_processing import save_processed_courses
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import json

def vectorize_courses(courses, batch_size=100):

    save_processed_courses(courses)

    embedding_dimension = 1536

    collections = qdrant_client.get_collections().collections
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=embedding_dimension,
                distance=Distance.COSINE
            )
        )

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        courses = json.load(f)

    points = []
    for idx, course in enumerate(courses):
        text = f"{course['courseTitle']}. {course['courseDescription']}"
        response = openai_client.embeddings.create(
            model=AI_model,
            input=text
        )
        embedding = response.data[0].embedding
        course_id = hashlib.md5(course['courseCode'].encode()).hexdigest()
        point = PointStruct(
            id=course_id,
            vector=embedding,
            payload=course
        )
        points.append(point)
        print(f"{idx} Course")

    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        qdrant_client.upsert(collection_name=collection_name, points=batch)
        print(f"Upserted batch {i // batch_size + 1}")