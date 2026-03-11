#tools/healthcare_tools.py
import sqlite3
import os 
import platform
import subprocess
from datetime import datetime
import webbrowser 
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt


DB_PATH = 'data/patient_records.db'

def get_patient_history(patient_name: str)->str:
    """
    Retrieves patients medical history from the real data base
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT history FROM patients WHERE LOWER(name) = ?",(patient_name.lower(),))
        result = cursor.fetchone()
        return result[0] if result else f"no record found for '{patient_name}'."
    

def calculate_vitals_risk(heart_rate: int, temperature:float)->str:
    """
    calculate risk level based on heart rate and body temperature.
    """
    is_high_hr = heart_rate > 100 or heart_rate < 50
    is_high_temp = temperature > 38.0 or temperature < 35.54

    if is_high_hr or is_high_temp :
        return  "RISK LEVEL: HIGH. Immediate clinical review is recommended due to abnormal vitals."
    return "RISK LEVEL: LOW . Vitals are within acceptible triage ranges.Continue to Monitor." 
    

#
def save_patient_vitals(patient_name: str, heart_rate: int,temperature: float)->str:
    """
    Saves new vitals for a patient into the database.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE patients 
            SET last_heart_rate = ?, last_temperature = ?
            WHERE LOWER(name) = ?''', (heart_rate, temperature, patient_name.lower()))
        
        if conn.total_changes > 0:
            conn.commit()
            return f"Vitals recorded for {patient_name}: HR {heart_rate}, Temp{temperature}."
        else:
            return f"Could not find patient '{patient_name}' to update ."

def add_new_patient(name:str, history: str = "New patient ,no history recorded .")->str:
    """ Adds a completely new patient to the Database ."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO patients (name, history)
                VALUES (?, ?)
            ''', (name, history))
            if conn.total_changes > 0:
                conn.commit()
                return f"Successfully registered '{name}' into the data base."
            else:
                return f"Patient '{name}' is already in the Database. "
    except Exception as e:
        return f"Error adding patient: {str(e)}"
    
def send_emergency_alert(patient_name: str, vitals: str) -> str:
    """Fixed Dispatch with visible button and UTF-8 encoding."""
    ack_file = os.path.abspath(f"data/doctor_ack.html")
    dispatch_file = os.path.abspath(f"data/dispatch.html")

    
    # FIX: Added encoding='utf-8' to handle the ✅ emoji
    with open(ack_file, "w", encoding='utf-8') as f:
        f.write(f"<html><body style='background:#004d40;color:white;text-align:center;padding:100px;'><h1>✅ ACKNOWLEDGMENT SENT</h1><p>Dr. Kapoor is arriving for {patient_name}.</p></body></html>")
    ack_url_path = ack_file.replace('\\', '/')
    dispatch_html = f"""
    <html><body style="background:#b71c1c;color:white;font-family:sans-serif;text-align:center;padding:50px;">
        <h1>🚨 EMERGENCY DISPATCH 🚨</h1>
        <div style="border:2px solid white;padding:20px;margin:20px;font-size:1.5em;">
            PATIENT: {patient_name.upper()}<br>CURRENT VITALS: {vitals}
        </div>
        <a href="file:///{ack_url_path}" style="background:white;color:#b71c1c;padding:20px;text-decoration:none;font-weight:bold;border-radius:10px;display:inline-block;">ACKNOWLEDGE & ACCEPT CASE</a>
    </body></html>
    """
    with open(dispatch_file, "w", encoding='utf-8') as f:
        f.write(dispatch_html)
    
    webbrowser.open(f"file:///{dispatch_file}")
    return "Dispatch sent successfully."
    
def generate_vitals_trend_chart(patient_name: str)-> str:
    """Generates a clinical chart with two lines: Temp (Red) and HR(Blue)
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT last_temperature, last_heart_rate FROM patients WHERE LOWER(name) = ?", (patient_name.lower(),))
            result = cursor.fetchone()

        if not result or result[0] is None:
            return f"Error: No data for {patient_name}."
        
        current_temp, current_hr = float(result[0]), int(result[1])
        base_temp, base_hr = 36.6, 72
        fig, ax1 = plt.subplots(figsize=(8, 5))
#TEMPERATURE AXIS(LEFT)
        ax1.set_ylabel('Temperature(°C)', color='red', fontweight='bold')
        ax1.plot(["Baseline", "Current"], [base_temp, current_temp], color='red',marker='o', linewidth=3, label="Temp")
        ax1.tick_params(axis='y', labelcolor='red')
        ax1.set_ylim(34, 46)

 #HEART RATE AXIS(RIGHT)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Heart Rate (BPM)', color='blue', fontweight='bold')
        ax2.plot(["Baseline", "Current"], [base_hr, current_hr], color='blue',marker='s', linestyle='--', linewidth=3, label="HR")
        ax2.set_ylim(40, 180)

        plt.title(f"CLINICAL TREND:{patient_name.upper()}")
        fig.tight_layout()

        chart_filename = f"{patient_name.replace(' ', '_')}_chart.png"
        chart_path = os.path.abspath(f"data/{chart_filename}")
        plt.savefig(chart_path)
        plt.close()

        return chart_filename
    except Exception as e:
        return f"Chart Error:{str(e)}"

def generate_soap_note(patient_name: str, symptoms: str, vitals: str, risk: str, search_context: str) -> str:
    """Generates and adoptive SOAP note with UTF-8 encoding.
    """
    is_high_risk = "HIGH" in risk.upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if is_high_risk:
        assessment = f"HIGH Risk. Suspected{search_context}."
        plan = "Emergency Alert send to Dr.Kapoor"
    else:
        assessment = "Low Risk. Vitals stable. "
        plan = "Routine Monitoring."
    
    soap_text = f"S: {symptoms}\n0: {vitals}\nA: {assessment}\nP: {plan}"
    file_path = os.path.abspath(f"data/{patient_name.replace(' ', '_')}_SOAP_NOTE.txt")

    with open(file_path, "w", encoding='utf-8') as f:
        f.write(soap_text)
    return soap_text

def generate_clinical_dashboard(patient_name: str, soap_text: str, chart_filename: str) -> str:
    """Combines SOAP and Chart into the Unified View with UTF-8 support.""" 
   
    
    dashboard_path = os.path.abspath("data/clinical_dashboard.html")
    dashboard_path = os.path.abspath("data/clinical_dashboard.html")
    abs_chart_path = os.path.abspath(f"data/{chart_filename}")
    formatted_chart_path = abs_chart_path.replace('\\', '/')
    chart_url = f"file:///{formatted_chart_path}"
    
    html_content = f"""
    <html>
    <head><meta charset="UTF-8">
        <style>
            body {{ font-family: sans-serif; background: #f4f7f6; margin: 0; }}
            .header {{ background: #2c3e50; color: white; text-align: center; padding: 20px; }}
            .container {{ display: flex; padding: 20px; gap: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); flex: 1; }}
            pre {{ background: #fffde7; padding: 15px; border-left: 5px solid #fbc02d; white-space: pre-wrap; font-size: 1.1em; }}
        </style>
    </head>
    <body>
        <div class="header"><h1>AI CLINICAL COMMAND CENTER</h1><p>Patient: {patient_name.upper()}</p></div>
        <div class="container">
            <div class="card"><h2>Clinical Documentation (SOAP)</h2><pre>{soap_text}</pre></div>
            <div class="card"><h2>Vitals Trend Analysis</h2><img src="{chart_url}" width="100%"></div>
        </div>
    </body>
    </html>
    """
    with open(dashboard_path, "w", encoding='utf-8') as f:
        f.write(html_content)
    webbrowser.open(f"file:///{dashboard_path}")
    return "Clinical Dashboard generated."


  





    


