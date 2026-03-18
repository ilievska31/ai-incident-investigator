from memory.incident_store import search_similar

def memory_retriever(state):

    query = f"""
    Logs:
    {state.get("parsed_logs", "")}

    Stacktrace:
    {state.get("stacktrace_analysis", "")}

    Correlations:
    {state.get("correlations", "")}
    """

    results = search_similar(query)

    state["similar_incidents"] = [
        r.page_content for r in results
    ]

    return state