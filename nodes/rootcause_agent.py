
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.output_parsers import PydanticOutputParser
from schemas.incident_schema import IncidentReport

def rootcause_analyzer(state):

    prompt = ChatPromptTemplate.from_template(
    """
        Based on the provided log, stacktrace and corelation analysis do an in-depth investigation.

        LOG ANALYSIS
        {log_analysis}

        STACKTRACE ANALYSIS
        {stacktrace_analysis}

        CORRELATION ANALYSIS
        {correlation_analysis}

        Determine the root cause.
        {format_instructions}
    """)

    parser = PydanticOutputParser(pydantic_object=IncidentReport)
    format_instructions = parser.get_format_instructions()

    messages = prompt.format_messages(
        log_analysis=state["log_analysis"],
        stacktrace_analysis=state["stacktrace_analysis"],
        correlation_analysis=state["correlation_analysis"],
        format_instructions=format_instructions
    )

    model = ChatOllama(
        model="llama3",
        temperature=0,
        format="json"
    )

    response = model.invoke(messages)
    incident = parser.parse(response.content)

    return {"report":incident}
