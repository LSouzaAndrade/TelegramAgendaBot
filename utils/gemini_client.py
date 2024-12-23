import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.gemini_function_calling import tools_parameters
from utils.gemini_function_calling import *
from vertexai.generative_models import Part


load_dotenv()
GOOGLE_GEMINI_API_KEY = os.environ['GOOGLE_GEMINI_API_KEY']
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

model_name = 'models/gemini-1.5-flash'
tool_config, tools = tools_parameters('auto')
system_instruction = f'''Você faz parte de uma API de sistema de reservas.
                        Não pergunte por todas informações faltantes de uma vez, solicite uma a uma.
                        Sua tarefa é agendar objetos conforme solicitado.
                        Não realize nenhuma outra tarefa ou fale sobre outros assuntos.
                        Não faça suposições.
                        Sempre valide as informações com o usuário antes de realizar a chamada da função.
                        Garanta que tenham sido informadas as horas de retirada e devolução do objeto.
                        Hoje é: {datetime.now().strftime('%d-%m-%Y')}'''

def initialize_chat_instance(model_name=model_name, tools=tools, system_instruction=system_instruction):
    model = genai.GenerativeModel(model_name=model_name, tools=tools, system_instruction=system_instruction)
    chat = model.start_chat()
    return chat

if 'chat' not in globals():
    chat = initialize_chat_instance()

def get_chat_response(message_content, chat=chat, tool_config=tool_config):
    result = chat.send_message(message_content, tool_config=tool_config)
    if result.parts[0].function_call:
        function_name = result.parts[0].function_call.name
        kwargs = result.parts[0].function_call.args
        if function_name in function_map:
            function = function_map[function_name]
            function_output = function(**kwargs)
            result = chat.send_message(str(function_output))
    if result.parts[0].text:
        response = str(result.parts[0].text)
    return response
