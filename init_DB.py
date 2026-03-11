#Google_ADK_HEALTHAGENT/init_DB.py
import sqlite3
import os

#Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

def setup_database():
    conn = sqlite3.connect('data/patient_records.db')
    cursor = conn.cursor()
#CREATING THE TABLLE patients
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS  patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        history TEXT,
        last_heart_rate  INTEGER,
        last_temperature REAL)''')
#inserting initial data
    inital_patients = [
        ('John Doe', 'History of Hyper-Tension.Last visit:3 months ago.', 72 , 36.6 ),
        ('Smith Williams', 'No chronic conditions. Allergic to Pencilin.', 85 , 37.0)
    ]
    cursor.executemany('INSERT OR IGNORE INTO patients(name, history, last_heart_rate, last_temperature ) VALUES(?, ?, ?, ?)', inital_patients)
    conn.commit()
    conn.close()
    print("Database initialized successfully at data/patient_records.db")

if __name__ == "__main__":
    setup_database()