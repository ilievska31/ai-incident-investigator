import ollama

def analyze_root_cause(log_analysis, trace_analysis):

    prompt = f"""
        You are a senior production incident investigator.

        LOG ANALYSIS
        {log_analysis}

        STACKTRACE ANALYSIS
        {trace_analysis}

        Tasks:

        1. Determine the most likely root cause
        2. Explain how the failure occurred
        3. Suggest what to fix

        Return sections:

        Incident Summary
        Root Cause
        What to Fix
        Next Debugging Steps
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]