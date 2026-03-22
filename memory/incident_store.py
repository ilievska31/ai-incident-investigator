from schemas.incident_schema import IncidentReport
from .vector_store import get_vectorstore
from .embeddings import get_embeddings
import math

vectorstore = get_vectorstore()
embeddings_model = get_embeddings()


def incident_to_document(incident:IncidentReport) ->str:
    return f""""
    Summary: 
    {incident.summary}

    Root cause:
    {incident.root_cause}

    Evidence:
    {incident.evidence}

    Failure Chain:
    {incident.failure_chain}

    Debugging Steps: 
    {incident.debugging_steps}
    """

def store_incident(incident: IncidentReport):
    doc = incident_to_document(incident)
    vectorstore.add_texts(
        texts=[doc],
        metadatas=[{
            "summary": incident.summary,
            "root_cause": incident.root_cause
        }]
    )

    vectorstore.persist()
    
def deduplicate(results, similarity_threshold=0.9):
    unique = []

    for item in results:
        is_duplicate = False

        for existing in unique:
            if item["content"][:200] == existing["content"][:200]:
                is_duplicate = True
                break

        if not is_duplicate:
            unique.append(item)

    return unique

def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(x*x for x in b))
    return dot / (norm_a * norm_b + 1e-8)

def diversify(results, query, max_items=3, lambda_param=0.7):
    if not results:
        return []

    query_embedding = embeddings_model.embed_query(query)

    for item in results:
        item["embedding"] = embeddings_model.embed_query(item["content"])

    selected = []

    while len(selected) < max_items and results:
        best_item = None
        best_score = -float("inf")

        for item in results:
            relevance = cosine_similarity(query_embedding, item["embedding"])

            if not selected:
                diversity_penalty = 0
            else:
                max_sim_to_selected = max(
                    cosine_similarity(item["embedding"], s["embedding"])
                    for s in selected
                )
                diversity_penalty = max_sim_to_selected

            score = lambda_param * relevance - (1 - lambda_param) * diversity_penalty

            if score > best_score:
                best_score = score
                best_item = item

        selected.append(best_item)
        results.remove(best_item)

    return selected

def search_similar(query: str, k: int = 8, score_threshold: float = 0.75):
    results = vectorstore.similarity_search_with_score(query, k=k)

    filtered = []

    for doc, score in results:
        similarity = 1 - score

        if similarity >= score_threshold:
            filtered.append({
                "content": doc.page_content,
                "similarity": similarity,
                "metadata": doc.metadata
            })

    filtered.sort(key=lambda x: x["similarity"], reverse=True)

    filtered = diversify(filtered, query, max_items=3)

    return [item["content"] for item in filtered]
