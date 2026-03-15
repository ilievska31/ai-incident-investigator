import ollama

def analyze_logs(logs):
    prompt = f"""
        You are analyxin production logs. 
        
        LOG EVENTS
        {logs}

        Tasks: 

        1. Extract key events
        2. Identify warnings and errors
        3. Summarize what happened in the system

        Return sections:

        Key Events
        Detected Errors
        Observations
    """
    
    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user", "content":prompt}]
    )

    return response["message"]["content"]