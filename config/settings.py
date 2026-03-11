# import os
# from dotenv import load_dotenv

# load_dotenv()

# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# #MODEL_NAME = 'gemini-1.5-flash-latest'
# MODEL_NAME = 'gemini-1.5-flash-002' 
# # Or use 'gemini-1.5-flash-002'

# list_models.py
#from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
#client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MODEL_NAME = "gemini-3-flash-preview" 
#for model in client.models.list():
   # print(f"Model Name: {model.name} - Supported Methods: {model.supported_methods}")
    #print(f"Model Name: {model.name} - Supported Actions: {model.supported_actions}")