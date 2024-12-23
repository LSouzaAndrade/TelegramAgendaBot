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
    OBJECT_1 = 'Apontador'
    OBJECT_2 = 'Borracha'
    OBJECT_3 = 'Caneta'

def schedule_object(reservation_object: Objects, start_datetime: str, end_datetime: str) -> dict:
    """
    Schedule the object according to the information given.

    Args:
        reservation_object (Enum): The object to be reserved.
        start_datetime (str): Reservation start in ISO 8601 format (yyyy-mm-dd HH:MM).
        end_datetime (str): Reservation end in ISO 8601 format (yyyy-mm-dd HH:MM).

    Returns:
        operation_result (bool): True if the reservation was successful, False otherwise.
    """
    return {'operation_result': False}

function_map = {
    'schedule_object': schedule_object
}

__all__ = ['schedule_object', 'function_map']