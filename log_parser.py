def parse_logs(text):
    lines = text.split("\n")

    relevant_levels = ["ERROR", "WARN", "Exception", "FATAL"]
    important_logs = []
    stacktrace_lines = []

    for line in lines:
        if any(level in line for level in relevant_levels):
            important_logs.append(line)
        if "Exception" in line or "at " in line:
            stacktrace_lines.append(line)
    
    return {
        "important_logs": "\n".join(important_logs),
        "stacktrace_lines": "\n".join(stacktrace_lines)
    }