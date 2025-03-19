from recommendation_server.app.data_pre_processing import save_processed_courses
import os
import openai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import json

qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        https=True
    )

openai_client = openai.Client(
        api_key=os.getenv("OPENAI_API_KEY")
    )

def vectorize_courses(courses):

    save_processed_courses(courses)

    load_dotenv(".env")

    collection_name = "courses_collection"
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
            id=idx,  # TODO CHANGE TO UUID LATER
            vector=embedding,
            payload=course
        )
        points.append(point)

    qdrant_client.upsert(collection_name=collection_name, points=points)