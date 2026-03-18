from typing import TypedDict, List
from schemas.incident_schema import IncidentReport

class IncidentState(TypedDict):
    logs: str
    parsed_logs: str
    stacktrace: str
    log_analysis: str
    stacktrace_analysis: str
    correlation_analysis: str
    report: IncidentReport
    similar_incidents: List[str] = []
