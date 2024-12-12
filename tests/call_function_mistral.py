import os
import json
import mistralai
from dotenv import load_dotenv
import time
import csv
import itertools
import sys
import threading

load_dotenv()

API_KEY = os.getenv("CallFunction_MISTRAL_API_KEY")
if not API_KEY:
    print("Erreur : Clé API manquante. Veuillez définir la variable d'environnement 'CallFunction_MISTRAL_API_KEY'.")
    sys.exit(1)

try:
    with open("tests/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Erreur : Le fichier 'tests/data.json' est introuvable.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Erreur : Le fichier 'tests/data.json' contient du JSON invalide.")
    sys.exit(1)

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
    },
    {
        "type": "function",
        "function": {
            "name": "explain_scientific_process",
            "description": "Fournit une explication scientifique détaillée de la formation moléculaire.",
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

output_file = "output.csv"
if not os.path.exists(output_file):
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Molecule", "Basic Explanation", "Scientific Explanation"])

def display_molecules(data):
    print("\n--- Molécules disponibles ---")
    for idx, molecule in enumerate(data, start=1):
        print(f"{idx}. {molecule['name']} (Formule : {molecule['formula']})")

def loading_animation(stop_event):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\rTraitement en cours... {c}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rTraitement terminé!   \n')

def send_request_with_retry(client, model, messages, tools, tool_choice='any', max_retries=5, backoff_factor=2, max_tokens=2000):
    retries = 0
    while retries < max_retries:
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        try:
            response = client.chat.complete(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                max_tokens=max_tokens,
                temperature=0.7
            )
            stop_event.set()
            loading_thread.join()
            return response
        except mistralai.models.sdkerror.SDKError as e:
            stop_event.set()
            loading_thread.join()
            if e.status_code == 429:
                retries += 1
                wait_time = backoff_factor ** retries
                print(f"\nDélai d'attente de {wait_time} secondes en raison du dépassement de la limite de requêtes.")
                time.sleep(wait_time)
            else:
                print(f"\nErreur de l'API: {e}")
                raise e
    raise Exception("Max retries exceeded")

def process_messages(messages):
    response = send_request_with_retry(client, model, messages, tools)
    print("Réponse brute de l'API :", response)
    
    if not response.choices or not response.choices[0].message:
        print("Erreur : Réponse vide de l'API.")
        return messages, "Réponse incomplète"
    
    message = response.choices[0].message
    if hasattr(message, 'tool_calls') and message.tool_calls:
        # Handle tool_calls
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"Appel de fonction détecté : {function_name} avec les paramètres {function_args}")
            # Exécuter la fonction locale
            if function_name == "explain_molecule_formation":
                function_result = explain_molecule_formation(**function_args)
            elif function_name == "explain_scientific_process":
                function_result = explain_scientific_process(**function_args)
            else:
                print(f"Fonction inconnue : {function_name}")
                function_result = "Fonction inconnue."
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_result)
            })
        return messages, None  # Continue processing
    else:
        explanation = message.content.strip() or "Réponse incomplète"
        print("Explication générée par Mistral :", explanation)
        return messages, explanation

def explain_molecule_formation(molecule_name, components):
    explanation = (
        f"La molécule {molecule_name} est formée par la combinaison de {', '.join(components)}. "
        f"Les composants se lient par des liaisons covalentes pour créer une structure stable."
    )
    return {"explanation": explanation}

def explain_scientific_process(molecule_name, components):
    explanation = (
        f"La formation de la molécule {molecule_name} à partir de ses composants {', '.join(components)} "
        f"implique plusieurs interactions atomiques et la formation de liaisons chimiques spécifiques. "
        f"Les électrons sont partagés entre les atomes pour établir des liaisons covalentes fortes, "
        f"contribuant ainsi à la stabilité de la molécule résultante."
    )
    return {"explanation": explanation}

while True:
    display_molecules(data)
    choice = input("\nEntrez le numéro de la molécule à expliquer ou 'q' pour quitter : ").strip().lower()
    if choice == 'q':
        print("Arrêt du programme.")
        break
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(data):
            molecule = data[choice]
            molecule_name = molecule["name"]
            components = [component["name"] for component in molecule["components"]]
            print(f"\nDemande d'explication pour : {molecule_name} avec les composants {components}")

            messages = [
                {
                    "role": "user",
                    "content": f"Expliquez comment {molecule_name} est formée à partir de ses composants : {', '.join(components)}."
                }
            ]

            messages, basic_explanation = process_messages(messages)

            while basic_explanation is None:
                messages, basic_explanation = process_messages(messages)

            scientific_messages = [
                {
                    "role": "user",
                    "content": f"Fournissez une explication scientifique détaillée de la formation de la molécule {molecule_name} "
                               f"à partir de ses composants : {', '.join(components)}. Incluez les interactions atomiques, "
                               f"les types de liaisons chimiques, les énergies de liaison, et les propriétés moléculaires impliquées."
                }
            ]
            messages = scientific_messages

            scientific_response = process_messages(messages)

            scientific_explanation = scientific_response[1]

            while scientific_explanation is None:
                scientific_response = process_messages(scientific_response[0])
                scientific_explanation = scientific_response[1]

            with open(output_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([molecule_name, basic_explanation, scientific_explanation])

            print(f"\nExplications enregistrées pour {molecule_name}.\n")
        else:
            print("Numéro invalide, veuillez réessayer.")
    except ValueError:
        print("Entrée invalide, veuillez entrer un numéro.")
    except mistralai.models.sdkerror.SDKError as e:
        print(f"Erreur de l'API: {e}")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
