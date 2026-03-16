import ollama
from rich import print
# from log_parser import parse_logs
# from agents.log_agent import analyze_logs
# from agents.stacktrace_agent import analyze_stacktrace
# from agents.rootcause_agent import analyze_root_cause
from langgraph.graph import StateGraph, START, END
from state import IncidentState

from nodes.parsing_agent import parser
from nodes.log_agent import log_analyzer
from nodes.stacktrace_agent import stacktrace_analyzer
from nodes.correlation_agent import correlation_analyzer
from nodes.rootcause_agent import rootcause_analyzer

def load_file(path):
    with open(path, "r") as f:
        return f.read()
    
#logs = load_file("logs.txt")

# parsedLogs = parse_logs(logs)


# print("Analyzing logs...")
# log_analysis = analyze_logs(parsedLogs["important_logs"])

# print("Analyzing stacktrace")
# stacktrace_analysis=analyze_stacktrace(parsedLogs["stacktrace_lines"])

# print("Detirmining rootcause")
# report = analyze_root_cause(log_analysis,stacktrace_analysis)

# print("\n Incident report \n")
# print(report)

graph = StateGraph(IncidentState)

graph.add_node("parser", parser)
graph.add_node("log_analyzer", log_analyzer)
graph.add_node("stacktrace_analyzer", stacktrace_analyzer)
graph.add_node("correlation_analyzer", correlation_analyzer)
graph.add_node("rootcause_analyzer", rootcause_analyzer)

graph.add_edge(START, "parser")
graph.add_edge("parser", "log_analyzer")
graph.add_edge("parser", "stacktrace_analyzer")
graph.add_edge("log_analyzer", "correlation_analyzer")
graph.add_edge("stacktrace_analyzer", "correlation_analyzer")
graph.add_edge("correlation_analyzer", "rootcause_analyzer")
graph.add_edge("rootcause_analyzer", END)

app = graph.compile()

logs = load_file("logs.txt")
result = app.invoke({"logs" :logs})

print(result["report"])