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
system_instruction = f'''Você faz parte de uma API de sistema de reservas.
                         Sua tarefa é agendar objetos conforme solicitado.
                         Não realize nenhuma outra tarefa ou fale sobre outros assuntos.
                         Não faça suposições.
                         Sempre pergunte por qualquer informação ausente, uma por vez.
                         Sempre valide as informações com o usuário antes de realizar a chamada da função.
                         Hoje é: {datetime.now().strftime('%d-%m-%Y')}'''

def initialize_chat_instance(model_name=model_name, tools=tools, system_instruction=system_instruction):
    model = genai.GenerativeModel(model_name=model_name, tools=tools, system_instruction=system_instruction)
    chat = model.start_chat()
    return chat

if 'chat' not in globals():
    chat = initialize_chat_instance()

def get_chat_response(message_content, chat=chat, tool_config=tool_config):
    response = chat.send_message(message_content, tool_config=tool_config)
    return response

