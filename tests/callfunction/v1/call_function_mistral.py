import os
import json
import mistralai
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("CallFunction_MISTRAL_API_KEY")

with open("tests/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

molecule_name = data.get("name", "Nom inconnu")
components = [component.get("name", "Inconnu") for component in data.get("components", [])]

client = mistralai.Mistral(api_key=API_KEY)
model = "mistral-large-latest"

tools = [
    {
        "type": "function",
        "function": {
            "name": "explain_molecule_formation",
            "description": "Explique comment la molécule est formée à partir de ses composants.",
            "parameters": {
                "type": "object",
                "properties": {
                    "molecule_name": {"type": "string", "description": "Le nom de la molécule."},
                    "components": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Les noms des composants de la molécule."
                    }
                },
                "required": ["molecule_name", "components"]
            }
        }
    }
]

messages = [
    {
        "role": "user",
        "content": f"Expliquez comment {molecule_name} est formée à partir de ses composants : {', '.join(components)}."
    }
]

def send_request_with_retry(client, model, messages, tools, tool_choice, max_retries=5, backoff_factor=2):
    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.complete(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice
            )
            return response
        except mistralai.models.sdkerror.SDKError as e:
            if e.status_code == 429:  # Rate limit exceeded
                retries += 1
                wait_time = backoff_factor ** retries
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded")

response = send_request_with_retry(client, model, messages, tools, "any")

tool_call = response.choices[0].message.tool_calls[0]
function_name = tool_call.function.name
function_params = json.loads(tool_call.function.arguments)

def explain_molecule_formation(molecule_name, components):
    explanation = (
        f"La molécule {molecule_name} est formée par la combinaison de {components[0]} et {components[1]}. "
        f"L'hydrogène se lie avec l'oxygène pour former des liaisons covalentes, créant ainsi une molécule d'eau stable."
    )
    return json.dumps({"explanation": explanation})

function_result = explain_molecule_formation(**function_params)
messages.append({"role": "user", "content": json.loads(function_result)["explanation"]})
final_response = client.chat.complete(
    model=model,
    messages=messages
)

print("Explication générée par Mistral :", final_response.choices[0].message.content)
