import ollama

def rootcause_analyzer(state):
    prompt = f"""
        Based on the provided log, stacktrace and corelation analysis do an in-depth invedtigation.

        LOG ANALYSIS
        {state["log_analysis"]}

        STACKTRACE ANALYSIS
        {state["stacktrace_analysis"]}

        CORRELATION ANALYSIS
        {state["correlation_analysis"]}

        Determine:
        1. Summary of events
        2. Root cause
        3. What to fix
        4. Debugging steps
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return {"report": response["message"]["content"]}

