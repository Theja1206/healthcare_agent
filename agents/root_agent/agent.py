#agents/root_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool, google_search, AgentTool
from agents.health_agent.agent import root_agent as health_specialist 


search_agent = LlmAgent(
    name="search_specialist",
    model="gemini-3-flash-preview",
    tools=[google_search],
    instruction=""" 
    you are a web search expert .use 'google_search' to find the facts """
)


root_agent = LlmAgent(
    name="root_agent", 
    model="gemini-3-flash-preview", 
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=health_specialist)
    ],
    instruction="""
    You are the lead clinical coordinator.
    1. DATABASE & DOCUMENTATION : For vitals, history, trend charts,SOAP notes, call 'health_triage_agent'.
    2. RESEARCH : For flu trends or symptoms ,call 'search_specialist'.
    WORK FLOW FOR NEW VITALS :
    - If a user provides new vitals(like Temp and HR), FIRST call 'health_triage_agent' to save the data and generate clinical documents(chart and SOAP notes).
    - SECOND call 'search_specialist' to get local health context.
    - FINALLY, summarise everything for the user,confirming that the chart and SOAP notes have been opened on the clinical workstation
    """
)

