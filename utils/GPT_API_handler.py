import json
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

class ChatInstance:
    def __init__(self, model, api_key=api_key, function_map={}, system_prompt=None, tools=None):
        if api_key is None:
            raise ValueError("API key is required. Set it via the OPENAI_API_KEY environment variable or pass it explicitly.")
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = [{'role': 'system', 'content': system_prompt}] if system_prompt else []
        self.function_map = function_map
        self.model = model
        self.tool_choice = None
        self.tools = tools

    def send_message(self, message):
        self.conversation_history.append({'role': 'user', 'content': message})
        response = self.conversation_completion()
        if response.tool_calls:
            response = self.handle_tool_call(response.tool_calls)
        return response.content

    def set_tool_choice(self, choice):
        tool_names = []
        if self.tools:
            tool_names = [tool['function']['name'] for tool in self.tools]
        if choice in [None, 'none', 'auto', 'required'] + tool_names:
            if choice in tool_names:
                self.tool_choice = {"type": "function", "function": {"name": choice}}
            else:
                self.tool_choice = choice
        else:
            raise Exception('Invalid mode. Choose from: None, "none", "auto", "required", or one of the tool names.')
        
    def handle_tool_call(self, tool_calls):
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_kwargs = json.loads(tool_call.function.arguments)
            tool_result = None
            if tool_name in self.function_map:
                tool_result = self.function_map[tool_name](**tool_kwargs)
            function_call_result_message = {
                "role": "tool",
                "content": json.dumps(tool_result),
                "tool_call_id": tool_call.id
            }
            self.conversation_history.append(function_call_result_message)
        response = self.conversation_completion()
        if response.tool_calls:
            response = self.handle_tool_call(response.tool_calls)
        return response

    def conversation_completion(self):
        if self.tools == None:
            tool_choice = None
        else:
            tool_choice = self.tool_choice
        completion = self.client.chat.completions.create(
            model=self.model, 
            messages=self.conversation_history,
            tool_choice=tool_choice,
            tools=self.tools
        )
        response = completion.choices[0].message
        self.conversation_history.append(response)
        return response
    