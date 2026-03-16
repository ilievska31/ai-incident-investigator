from typing import TypedDict

class IncidentState(TypedDict):
    logs: str
    important_logs: str
    stacktrace: str
    log_analysis: str
    stacktrace_analysis: str
    correlation_analysis: str
    report: str
