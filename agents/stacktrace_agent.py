import ollama

def analyze_stacktrace(trace):

    prompt = f"""
        You are analyzing stack traces extracted from logs.

        STACK TRACE
        {trace}

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
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]