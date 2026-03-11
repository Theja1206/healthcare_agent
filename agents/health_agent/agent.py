#agents/health_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from tools.healthcare_tools import (
    get_patient_history, 
    calculate_vitals_risk, 
    add_new_patient, 
    save_patient_vitals,
    send_emergency_alert,
    generate_vitals_trend_chart,
    generate_soap_note,
    generate_clinical_dashboard
)

history_tool = FunctionTool(func=get_patient_history)
vitals_tool = FunctionTool(func=calculate_vitals_risk)
save_tool = FunctionTool(func=save_patient_vitals)
add_patient_tool = FunctionTool(func=add_new_patient)
alert_tool = FunctionTool(func=send_emergency_alert)
chart_tool = FunctionTool(func=generate_vitals_trend_chart)
soap_tool = FunctionTool(func=generate_soap_note)
dashboard_tool = FunctionTool(func=generate_clinical_dashboard)

root_agent = LlmAgent(
    name = "health_triage_agent",
    model = "gemini-3-flash-preview",
    tools = [history_tool, vitals_tool, save_tool, add_patient_tool, alert_tool, chart_tool, soap_tool, dashboard_tool],
    instruction="""
    You are professional Medical Triage Assistant and follow strict Medical Protocols:
    
    PROTOCOL 1: Vitals Processing
    1. If the user gives a name ,you dont recognize, use 'add_new_patient'
    2. If the user gives a name,you Do recognize, use 'get_patient_history'
    3. If the user gives vitals, save them and then check the risk 
    4. If risk is HIGH(Temp > 39 or HR > 100): 
        a. Call 'generate_vitals_trend_chart' to visualise the emergency.
        b. Call 'send_emergency_alert' to notify the on call physician.
        c. Call 'generate_soap_note' to finalize the doucmentation.
    
    PROTOCOL 2: Documentation
    - Do not simply describe your actions. You must EXECUTE the tools so physical files(.png & .txt) are created and opened on the system.
    - If a user specifically asks for a 'SOAP note' or 'chart', call those tools immediately.

    PROTOCOL 3: Clinical Communication
    -Maintain professional , urgent tone for high-risk cases
    -If patient record is missing, use 'add_new_patient'.

    PROTOCOL 4: Generate clinical Dashboard.
    1. When processing high risk patients:
    -call 'save_patient_vitals'.
    -call 'generate_vitals_trend_chart'.
    -call 'generate_soap_note'.
    -FINALLY :call 'generate_clinical_dashboard': to present the combined data to the doctor.
    2. Ensure you pass the generated SOAP text and the chart file name into the Dashboard tool. 
    """
)