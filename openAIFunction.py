import json
import openai
from fetchScheduleData import scheduleQuestions, greetings
from bookEvent import schedule_meeting

# Set OpenAI API key
openai.api_key = "sk-proj-jUq8Zp6NtUJV4Frx7ynXT3BlbkFJUo8qsF1BPTGTrb1RGp0j"

# Function for bot interaction
def bot_calling_functions(user_prompt):
    print("In bot function")
    function_response = None
    
    # Construct user message
    messages = [{"role": "user", "content": user_prompt}]
    
    # Define available functions
    functions = [
        {
            "name": "greetings",
            "description": "Respond to basic questions/greetings",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Greetings",
                    },
                },
                "required": ["prompt"],
            },
        },
        {
            "name": "scheduleQuestions",
            "description": "Respond to questions related to schedule and availability",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Get day of the week from prompt for getting the availability details",
                    },
                    "available_time_slot": {"type": "string"},
                    "unavailability": {"type": "string"}
                },
                "required": ["prompt"],
            },
        },
        {
            "name": "schedule_meeting",
            "description": "Function to schedule a meeting on calendar when appropriate time, date, and meeting description are given",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Asking to schedule a meeting with meeting details",
                    },
                    "description": {"type": "string"},
                    "startTime": {"type": "string", "description": "Date and time in ISO String in PST timezone (-7:00)"},
                    "endTime": {"type": "string", "description": "Date and time in ISO String in PST timezone (-7:00)"},
                },
                "required": ["summary", "description", "startTime", "endTime"],
            }
        }
    ]
    
    # Call OpenAI's ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    # Process response
    response_message = response.choices[0].message
    
    if 'function_call' in response_message:
        function_name = response_message['function_call']['name']
        function_args = json.loads(response_message['function_call']['arguments'])

        # Map function names to actual functions
        available_functions = {
            "scheduleQuestions": scheduleQuestions,
            "schedule_meeting": schedule_meeting,
            "greetings": greetings
        }
        
        # Call the appropriate function
        function_to_call = available_functions.get(function_name)
        
        if function_to_call:
            function_response = function_to_call(**function_args)
            print("Function Response:", function_response)
            return function_response
        else:
            print("Error: Function '{}' not found.".format(function_name))
    else:
        print("Error: 'function_call' key not found in response.")

    return None

# Example usage
user_prompt = "Hello, how can I help you today?"
bot_calling_functions(user_prompt)



