def refine_analysis(state):
    state["retry_count"] = state.get("retry_count",0) + 1
    previous_report = state["report"].model_dump_json(indent=2)
    state["correlation_analysis"] += f"""
        PREVIOUS LOW_CONFIDENCE ANALYSIS
        {previous_report}
        Re-evaluate and improve the reasoning
    """
    return state
