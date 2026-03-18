from log_parser import parse_logs

def parser(state):
    parsed = parse_logs(state["logs"])
    
    return {
        "parsed_logs": parsed["parsed_logs"],
        "stacktrace": parsed["stacktrace_lines"]
    }