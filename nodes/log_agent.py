import ollama

def log_analyzer(state):
    prompt = f"""
        Analyze thes provided log events:
        
        LOGS 
        {state["parsed_logs"]}
        
        Return: 
        1. Key events 
        2. Detected errors
        3. Observations
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user", "content":prompt}]
    )

    return {"log_analysis": response["message"]["content"]}