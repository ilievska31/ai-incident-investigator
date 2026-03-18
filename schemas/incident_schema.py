from pydantic import BaseModel
from typing import List

class IncidentReport(BaseModel):
    summary: str
    root_cause: str
    evidence: List[str]
    failure_chain: List[str]
    debugging_steps: List[str]

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