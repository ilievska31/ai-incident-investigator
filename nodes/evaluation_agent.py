
def evaluate_confidence(state): 
    report = state["report"]
    
    if report.confidence < 0.6 and state.get("retry_count", 0) < 2:
        return { "retry": True }
    return { "retry": False }

