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


def generate_recommendations_from_passed_courses(passed_course_codes, possible_course_codes, top_k: int):

    passed_courses = qdrant_client.scroll(
        collection_name=collection_name,
        with_payload=["courseTitle", "courseDescription"],
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="courseCode",
                    match=MatchAny(any=passed_course_codes)
                )
            ]
        ),
    )

    all_results = []
    points, _ = passed_courses
    for point in points:
        description = point.payload.get("courseDescription")
        if description:
            all_results.extend(filter_search(possible_course_codes, description, top_k).points)
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
def filter_search(course_codes, query_text, top_k):
    search_response = openai_client.embeddings.create(
        model=AI_model,
        input=query_text
    )

    query_embedding = search_response.data[0].embedding
    query_filter = Filter(
        must=[
            FieldCondition(
                key="courseCode",
                match=MatchAny(any=course_codes)
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
