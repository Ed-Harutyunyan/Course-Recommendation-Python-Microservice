import json

from infisical_sdk import InfisicalSDKClient
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, HasIdCondition
import os
import openai
from dotenv import load_dotenv

# client = InfisicalSDKClient(host="https://app.infisical.com")
#
# client.auth.universal_auth.login(
#     client_id=os.getenv("INFISICAL_CLIENT_ID"),
#     client_secret=os.getenv("INFISICAL_CLIENT_SECRET")
# )
#
# secret = client.secrets.get_secret_by_name(
#     secret_name="OPENAI_API",
#     project_id=os.getenv("INFISICAL_PROJECT_ID"),
#     environment_slug="dev",
#     secret_path="/"
# )

load_dotenv("../../.env")

collection_name = "courses_collection"

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    https=True
)


openai_client = openai.Client(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_recommendations_by_keywords(query_text: str, top_k: int):

    search_response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query_text
    )
    query_embedding = search_response.data[0].embedding
    search_results = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
        query_filter=None
    )

    recommendations = []
    for result in search_results.points:
        recommendations.append({
            "id": result.id,
            "title": result.payload.get("title"),
            "description": result.payload.get("description")
        })

    return recommendations


def generate_recommendations_from_passed_courses(passed_ids, possible_ids, top_k: int):

    passed_courses = qdrant_client.retrieve(
        collection_name=collection_name,
        with_payload=["title", "description"],
        ids = passed_ids
    )

    all_results = []
    for point in passed_courses:
        description = point.payload.get("description")
        if description:
            search_response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=description
            )
            embedding = search_response.data[0].embedding

            query_filter = Filter(
                must=[
                    HasIdCondition(has_id=possible_ids)
                ]
            )

            search_results = qdrant_client.query_points(
                collection_name=collection_name,
                query=embedding,
                limit=top_k,
                query_filter=query_filter
            )

            all_results.extend(search_results.points)
        else:
            raise ValueError("Descriptions list cannot be empty or None")

    unique_results = {}
    for result in all_results:
        if result.id not in unique_results or result.score > unique_results[result.id].score:
            unique_results[result.id] = result

    final_results = sorted(unique_results.values(), key=lambda x: x.score, reverse=True)

    recommendations = []
    for result in final_results:
        recommendations.append({
            "id": result.id,
            "title": result.payload.get("title"),
            "description": result.payload.get("description"),
            "score": result.score
        })

    return recommendations

