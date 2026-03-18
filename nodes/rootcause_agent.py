import json
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from schemas.incident_schema import IncidentReport
from memory.incident_store import store_incident


import json
from schemas.incident_schema import IncidentReport

def safe_parse(response_text: str) -> IncidentReport:

    raw = json.loads(response_text)

    # unwrap if needed
    if "properties" in raw:
        raw = raw["properties"]

    # 🔥 fill missing fields
    raw.setdefault("summary", "")
    raw.setdefault("root_cause", "")
    raw.setdefault("evidence", [])
    raw.setdefault("failure_chain", [])
    raw.setdefault("debugging_steps", [])

    return IncidentReport.model_validate(raw)

def rootcause_analyzer(state):

    similar_incidents = "\n\n".join(state.get("similar_incidents", []))

    prompt = ChatPromptTemplate.from_template(
    """
You are an expert incident investigator.

Analyze the system failure using logs, stacktraces, and correlations.

Also consider similar past incidents for pattern recognition.

====================
LOG ANALYSIS
{log_analysis}

STACKTRACE ANALYSIS
{stacktrace_analysis}

CORRELATION ANALYSIS
{correlation_analysis}

SIMILAR PAST INCIDENTS
{similar_incidents}
====================

Instructions:
- Identify the true root cause (not just symptoms)
- Use similar incidents as supporting evidence when relevant
- Be precise and technical

Return ONLY valid JSON (no explanation, no markdown, no schema):

{{  
  "summary": "short high-level explanation",
  "root_cause": "exact technical cause",
  "evidence": ["log/stacktrace facts"],
  "failure_chain": ["step-by-step failure sequence"],
  "debugging_steps": ["actionable steps"]
}}
"""
    )

    messages = prompt.format_messages(
        log_analysis=state["log_analysis"],
        stacktrace_analysis=state["stacktrace_analysis"],
        correlation_analysis=state["correlation_analysis"],
        similar_incidents=similar_incidents
    )

    model = ChatOllama(
        model="llama3",
        temperature=0,
        format="json"
    ).with_structured_output(IncidentReport)

    response = model.invoke(messages)

    return {"report": response}