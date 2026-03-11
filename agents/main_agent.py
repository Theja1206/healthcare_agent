#agents/main_agent.py
from google import genai
from config.settings import GOOGLE_API_KEY, MODEL_NAME
from tools.calculator_tool import calculator
from tools.file_reader_tool import read_file

class MultiFunctionAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
    
    def process_query(self , user_input: str):
        """
        Multi-function AI Agent Logic
        """
        #Tool1:Calculator
        if "calculate" in user_input.lower():
            expression = user_input.lower().replace("calculate", "").strip()
            return calculator(expression)
        #Tool2:File Reader
        elif "read file" in user_input.lower():
            file_path =  user_input.lower().replace("read file","").strip()
            # file_path = user_input.strip()[5:].strip()
            return read_file(file_path)
        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=user_input
            )
            return response.text if response.text else "No response from AI"
        except Exception as e:
            return f"AI error:{str(e)}"