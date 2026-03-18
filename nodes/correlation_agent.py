import ollama 

def correlation_analyzer(state):
    prompt=f"""
        Based on the provided log analysis and stacktrace analysis, execute these tasks:
        1. Identify the relationship between the log events and the stacktrace
        2. Determine if the log events could explain the stacktrace 
        3. Explain the causal chain of events

        LOG ANALYSIS 
        {state["log_analysis"]}

        STACKTRACE ANALYSIS
        {state["stacktrace_analysis"]}
      """
    
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user","content":prompt}]

    )

    return {
        "correlation_analysis": response["message"]["content"]
    }