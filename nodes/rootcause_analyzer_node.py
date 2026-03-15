import ollama

def rootcause_analyzer_node(state):
    analyzed_logs_response = state["log_analysis"]
    analyzed_stacktrace_response = state["stacktrace_analysis"]

    prompt = f"""
        Based on the provided analyzed logs and the stack traces,
        determine a possible root cause and what to fix.

        ANALYZED LOGS 
        {analyzed_logs_response}

        ANALYZED STACK TRACES
        {analyzed_stacktrace_response}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return {"report": response["message"]["content"]}

