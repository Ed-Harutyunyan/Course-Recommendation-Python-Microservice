from qdrant_client.http.models import FieldCondition, MatchAny
from qdrant_client.models import Filter, HasIdCondition

from recommendation_server.app.config import openai_client, qdrant_client, collection_name, AI_model


def generate_recommendations_by_keywords(query_text: str, course_ids, top_k: int):

    search_results = filter_search(course_ids, query_text, top_k)

    recommendations = []
    for result in search_results.points:
        recommendations.append({
            "id": result.id,
            "courseCode": result.payload.get('courseCode'),
            "courseTitle": result.payload.get("courseTitle"),
            "courseDescription": result.payload.get("courseDescription"),
            "score": result.score
        })

    return recommendations


def generate_recommendations_from_passed_courses(passed_ids, possible_ids, top_k: int):

    passed_courses = qdrant_client.retrieve(
        collection_name=collection_name,
        with_payload=["courseTitle", "courseDescription"],
        ids = passed_ids
    )

    all_results = []
    for point in passed_courses:
        description = point.payload.get("courseDescription")
        if description:
            all_results.extend(filter_search(possible_ids, description, top_k).points)
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
            "courseCode": result.payload.get('courseCode'),
            "courseTitle": result.payload.get("courseTitle"),
            "courseDescription": result.payload.get("courseDescription"),
            "score": result.score
        })
    print(recommendations)
    return recommendations


#Helper
def filter_search(course_ids, query_text, top_k):
    search_response = openai_client.embeddings.create(
        model=AI_model,
        input=query_text
    )
    query_embedding = search_response.data[0].embedding
    query_filter = Filter(
        must=[
            FieldCondition(
                key="courseCode",
                match=MatchAny(any=course_ids)
            )
            # HasIdCondition(has_id=course_ids)
        ]
    )
    search_results = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
        query_filter=query_filter
    )
    return search_results
