import json
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from schemas.incident_schema import IncidentReport
from memory.incident_store import store_incident


import json
from schemas.incident_schema import IncidentReport

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
        - Assign a confidence score between 0 and 1
        - Base confidence on:
        * Strength of evidence
        * Consistency between logs and stacktrace
        * Similarity to past incidents
        * Presence of ambiguity
        - Be conservative: if uncertain, lower the score
        
        Confidence Guidelines:

        HIGH (0.8-1.0):
        - Clear exception + matching logs
        - Strong match with past incidents

        MEDIUM (0.5-0.8):
        - Partial match
        - Some ambiguity

        LOW (<0.5):
        - Missing stacktrace or unclear cause
        - Multiple competing explanations

        Return ONLY valid JSON (no explanation, no markdown, no schema):

        {{  
            "summary": "...",
            "root_cause": "...",
            "evidence": [...],
            "failure_chain": [...],
            "debugging_steps": [...],
            "confidence": 0.0,
            "confidence_reasoning: "..."
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