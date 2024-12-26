from utils.db_handler import insert_reservation, check_reservation_availability


function_map = {'insert_reservation': insert_reservation,
                'check_reservation_availability': check_reservation_availability}

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_reservation_availability",
            "description": "Checks if a reservation is available for a given object and time range.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_object": {
                        "type": "string",
                        "description": "The object for which the reservation is being made.",
                        "enum": ["Projetor", "Multímetro", "Carro"]
                    },
                    "start_datetime": {
                        "type": "string",
                        "description": "The start date of the reservation in the format 'YYYY-MM-DD HH:MM:SS'."
                    },
                    "end_datetime": {
                        "type": "string",
                        "description": "The end date of the reservation in the format 'YYYY-MM-DD HH:MM:SS'."
                    },
                },
                "required": ["reservation_object","start_datetime", "end_datetime"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "insert_reservation",
            "description": "Checks if a reservation is available for a given object and time range, and inserts it into the database if it is.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_object": {
                        "type": "string",
                        "description": "The object for which the reservation is being made.",
                        "enum": ["Projetor", "Multímetro", "Carro"]
                    },
                    "start_datetime": {
                        "type": "string",
                        "description": "The start date of the reservation in the format 'YYYY-MM-DD HH:MM:SS'."
                    },
                    "end_datetime": {
                        "type": "string",
                        "description": "The end date of the reservation in the format 'YYYY-MM-DD HH:MM:SS'."
                    },
                },
                "required": ["reservation_object","start_datetime", "end_datetime"],
                "additionalProperties": False
            }
        }
    }
]
