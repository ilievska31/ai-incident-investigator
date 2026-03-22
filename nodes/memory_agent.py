from memory.incident_store import search_similar

def memory_retriever(state):

    query = f"""
    Logs:
    {state.get("parsed_logs", "")}

    Stacktrace:
    {state.get("stacktrace_analysis", "")}

    Correlations:
    {state.get("correlation_analysis", "")}
    """
    results = search_similar(query)

    state["similar_incidents"] = results
    return state