import os
import warnings
import json
import openai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from sqlalchemy.engine import URL
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.chat_models import ChatOpenAI
from constants import APIKEY  # Ensure you have this file and variable

warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = "sk-proj-jUq8Zp6NtUJV4Frx7ynXT3BlbkFJUo8qsF1BPTGTrb1RGp0j"
openai.api_key = "sk-proj-jUq8Zp6NtUJV4Frx7ynXT3BlbkFJUo8qsF1BPTGTrb1RGp0j"

# Set Google Docs API credentials
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SERVICE_ACCOUNT_FILE = '/Users/krishnasit/Downloads/finalProject/Credentials.json'
document_id = '1DzSUZ-iSbVDQHqQ5fQ0n07uQ6PIjK1jIhgXzO2rGxQI'
creds = None

# Set up credentials and service
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    print(creds)

def fetch_google_docs(document_id):
    service = build("docs", "v1", credentials=creds)
    result = service.documents().get(documentId=document_id).execute()
    content = result.get('body').get('content', [])
    text_content = ''
    for elem in content:
        if 'paragraph' in elem:
            text = elem['paragraph']['elements'][0]['textRun']['content']
            text_content += text
    with open("/Users/krishnasit/Downloads/finalProject/prompt.txt", 'w') as f:
        f.write(text_content)
    return text_content

def greetings(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    model_response = completion.choices[0].message['content']
    return model_response

def scheduleQuestions(prompt):
    document_text = fetch_google_docs(document_id)
    embeddings = OpenAIEmbeddings()
    loader = TextLoader('/Users/krishnasit/Downloads/finalProject/prompt.txt', encoding='utf-8')
    index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])
    response = index.query(prompt, llm=ChatOpenAI())
    return response

def bot_calling_functions(userPrompt):
    messages = [{"role": "user", "content": userPrompt}]
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
                },
                "required": ["prompt"],
            },
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    response_message = response.choices[0].message

    if 'function_call' in response_message:
        function_name = response_message['function_call']['name']
        function_args = json.loads(response_message['function_call']['arguments'])

        available_functions = {
            "scheduleQuestions": scheduleQuestions,
            "greetings": greetings
        }

        function_to_call = available_functions[function_name]

        if function_name == "scheduleQuestions":
            function_response = function_to_call(
                prompt=function_args.get("prompt")
            )
        elif function_name == "greetings":
            function_response = function_to_call(
                prompt=function_args.get("prompt")
            )

        return function_response

    return response_message['content']

# Example usage
user_prompt = "Hello, how can I help you today?"
response = bot_calling_functions(user_prompt)
print(response)


