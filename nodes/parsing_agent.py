from log_parser import parse_logs

def parser(state):
    parsed = parse_logs(state["logs"])
    
    return {
        "important_logs": parsed["important_logs"],
        "stacktrace": parsed["stacktrace_lines"]
    }