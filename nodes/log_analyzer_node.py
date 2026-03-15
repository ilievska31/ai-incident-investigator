import ollama

def log_analyzer_node(state):
    logs = state["important_logs"]

    prompt = f"""
        Analyze thes provided log events:
        LOGS {logs}
        Return: Key events, Detected errors, Observations
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user", "content":prompt}]
    )

    return {"log_analysis": response["message"]["content"]}