import inspect
import sys
from google.generativeai.types import content_types


def function_calling_options():
    script = sys.modules[__name__]
    functions = []
    function_names = []
    for nome, func in inspect.getmembers(script, inspect.isfunction):
        if nome not in ['function_calling_options', 'tools_parameters']:
            function_names.append(nome)
            functions.append(func)
    return function_names, functions

def tools_parameters(mode):
    allowed_function_names, allowed_functions = function_calling_options()
    config = {
        'function_calling_config': {
            'mode': mode
        }
    }
    if mode == "any":
        config['function_calling_config']['allowed_function_names'] = allowed_function_names
    return content_types.to_tool_config(config), allowed_functions

# Exemplo de função disponível para o function calling:

from enum import Enum

class Objects(Enum):
    OBJECT_1 = 'BYD Dolphin Mini'
    OBJECT_2 = 'Volkswagen Gol'
    OBJECT_3 = 'Chevrolet S10'

def schedule_object(object: Objects, project_number: int, start_date: str, start_time: str, end_date: str, end_time: str):
    """
    Schedule the object according to the information given.

    Args:
        object (Enum): The object to be reserved.
        project_number (int): The project in which the object will be used.
        start_date (str): Reservation start date in dd-mm-yyyy format.
        start_time (str): Reservation start time in %H:%M format.
        end_date (str): Reservation end date in dd-mm-yyyy format.
        end_time (str): Reservation end time in %H:%M format.
    """
    print('Houve uma tentativa de function calling')