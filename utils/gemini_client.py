import google.generativeai as genai
import os
from dotenv import load_dotenv
from utils.gemini_function_calling import tools_parameters
from datetime import datetime

load_dotenv()
GOOGLE_GEMINI_API_KEY = os.environ['GOOGLE_GEMINI_API_KEY']
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

model_name = 'models/gemini-1.5-flash'
tool_config, tools = tools_parameters('auto')
system_instruction = f'''You are part of a reservation system API.
                        Your task is to schedule objects as requested. 
                        Do not perform any other tasks.
                        Do not make assumptions; always ask for any missing information.
                        Always validate the information with the user before making the function call.
                        Today's date is {datetime.now().strftime('%d-%m-%Y')}'''

def initialize_chat_instance(model_name=model_name, tools=tools, system_instruction=system_instruction):
    model = genai.GenerativeModel(model_name=model_name, tools=tools, system_instruction=system_instruction)
    chat = model.start_chat()
    return chat

if 'chat' not in globals():
    chat = initialize_chat_instance()

def get_chat_response(message_content, chat=chat, tool_config=tool_config):
    response = chat.send_message(message_content, tool_config=tool_config)
    return response

