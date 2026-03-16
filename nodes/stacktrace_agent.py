import ollama

def stacktrace_analyzer(state):
    prompt = f"""
        Analyze the stack traces extracted.

        STACK TRACES
        {state["stacktrace"]}

        Tasks:

        1. Identify the failing methods
        2. Identify the likely causes
        3. Identify which service or class is failing

        Return sections:

        Failure Location
        Probable Cause
        Code Areas to Inspect
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user", "content": prompt}]
    )

    return {"stacktrace_analysis": response["message"]["content"]}

    