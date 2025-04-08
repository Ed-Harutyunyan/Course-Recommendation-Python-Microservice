from infisical_sdk import InfisicalSDKClient

from recommendation_server.app.config import qdrant_client, openai_client, collection_name
from recommendation_server.app.data_pre_processing import save_processed_courses
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import json

def vectorize_courses(courses):

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

    with open("data/processed_courses.json", "r", encoding="utf-8") as f:
        courses = json.load(f)

    points = []
    for idx, course in enumerate(courses):
        text = f"{course['courseTitle']}. {course['courseDescription']}"
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        embedding = response.data[0].embedding
        point = PointStruct(
            id=course['id'],
            vector=embedding,
            payload=course
        )
        points.append(point)

    qdrant_client.upsert(collection_name=collection_name, points=points)