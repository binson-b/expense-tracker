
import settings
import json
from openai import OpenAI
# ollama is a library
from ollama import generate, GenerateResponse
# gsheet is a library for Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_gsheet_client():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(settings.GSHEET_KEYFILE_DICT, scope)
    sheet = gspread.authorize(creds).open(settings.GSHEET_NAME).get_worksheet(1)
    return sheet


openai_client = OpenAI(
  api_key=settings.OPENAI_API_KEY,
)

def ai_api_call(prompt):
    ai = None
    if settings.USE_OPENAI_API:
        ai = "openai"
        response = openai_api_call(prompt)
    elif settings.USE_OLLAMA_API:
        ai = "ollama"
        response = ollama_api_call(prompt)
    else:
        print("No AI API selected")
        return None

    if response is None:
        print("No response from AI API")
        return None

    print(f"Response from {ai} API:", response)
    return response

def openai_api_call(prompt):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None
    

def ollama_api_call(prompt):
    try:
        response: GenerateResponse = generate(model='llama3.2', prompt=prompt)
        if response is None:
            print("No response from Ollama API")
            return None
        return response.response

    except Exception as e:
        print(f"Error calling llama API: {e}")
        return None

def parse_expense_data(expense_data):
    try:
        # Assuming the response is in JSON format
        parsed_data = json.loads(expense_data)
        return parsed_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    
def record_expense(date, description, amount, payer):
    sheet = get_gsheet_client()
    if not sheet:
        print("Failed to get Google Sheets client")
        return False
    try:
        sheet.append_row([date, description, amount, payer])
    except Exception as e:
        print(f"Failed to record the expense. Error: {e}")
        return False
    return True