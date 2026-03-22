from pydantic import BaseModel
from typing import List

class IncidentReport(BaseModel):
    summary: str
    root_cause: str
    evidence: List[str]
    failure_chain: List[str]
    debugging_steps: List[str]
    confidence: float
    confidence_reasoning: str