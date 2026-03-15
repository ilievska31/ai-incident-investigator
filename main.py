import ollama
from rich import print
from log_parser import parse_logs
from agents.log_agent import analyze_logs
from agents.stacktrace_agent import analyze_stacktrace
from agents.rootcause_agent import analyze_root_cause

def load_file(path):
    with open(path, "r") as f:
        return f.read()
    
logs = load_file("logs.txt")

parsedLogs = parse_logs(logs)


print("Analyzing logs...")
log_analysis = analyze_logs(parsedLogs["important_logs"])

print("Analyzing stacktrace")
stacktrace_analysis=analyze_stacktrace(parsedLogs["stacktrace_lines"])

print("Detirmining rootcause")
report = analyze_root_cause(log_analysis,stacktrace_analysis)

print("\n Incident report \n")
print(report)
