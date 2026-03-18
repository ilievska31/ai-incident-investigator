from schemas.incident_schema import IncidentReport
from .vector_store import get_vectorstore

vectorstore = get_vectorstore()

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

def search_similar(query: str, k: int = 3):
    return vectorstore.similarity_search(query, k=k)
