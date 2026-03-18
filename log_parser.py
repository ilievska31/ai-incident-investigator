def parse_logs(text):
    lines = text.split("\n")

    relevant_levels = ["ERROR", "WARN", "Exception", "FATAL"]
    parsed_logs = []
    stacktrace_lines = []

    for line in lines:
        if any(level in line for level in relevant_levels):
            parsed_logs.append(line)
        if "Exception" in line or "at " in line:
            stacktrace_lines.append(line)
    
    return {
        "parsed_logs": "\n".join(parsed_logs),
        "stacktrace_lines": "\n".join(stacktrace_lines)
    }