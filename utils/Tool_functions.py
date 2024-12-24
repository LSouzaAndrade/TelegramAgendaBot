def get_weather(location, unit):
    print('Chamada de temperatura para', location, 'em', unit, 'executada.')
    return {'value': 25}

def get_stock_price(symbol):
    print('Chamada de preço de ação para', symbol, 'executada.')
    return {'value': 100}

function_map = {'get_weather': get_weather, 
                'get_stock_price': get_stock_price}

tools = [
  {
      "type": "function",
      "function": {
          "name": "get_weather",
          "strict": True,
          "parameters": {
              "type": "object",
              "properties": {
                  "location": {"type": "string"},
                  "unit": {"type": "string", "enum": ["c", "f"]},
              },
              "required": ["location", "unit"],
              "additionalProperties": False,
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "get_stock_price",
          "strict": True,
          "parameters": {
              "type": "object",
              "properties": {
                  "symbol": {"type": "string"},
              },
              "required": ["symbol"],
              "additionalProperties": False,
          },
      },
  },
]
