from qdrant_client import QdrantClient
import os
import openai
from dotenv import load_dotenv

def generate_recommendations(query_text: str, top_k: int = 3):

    load_dotenv(".env")

    collection_name = "courses_collection"

    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        https=True
    )

    openai_client = openai.Client(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    search_response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query_text
    )
    query_embedding = search_response.data[0].embedding
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )
    recommendations = []
    for result in search_results:
        recommendations.append({
            "id": result.id,
            "title": result.payload.get("title"),
            "description": result.payload.get("description"),
            "score": result.score
        })
    return recommendations