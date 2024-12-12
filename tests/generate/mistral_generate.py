from mistralai import Mistral
from dotenv import load_dotenv
import os
import json
import re

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API
api_key = os.environ.get("MISTRAL_API_KEY")
model = "mistral-large-latest"

# Vérifier que la clé API est présente
if not api_key:
    raise ValueError("La clé API MISTRAL_API_KEY est manquante dans les variables d'environnement.")

# Initialiser le client Mistral avec la clé API
client = Mistral(api_key=api_key)

# Préparer le contenu du message pour le modèle
messages = [
    {
        "role": "user",
        "content": (
            "En utilisant les molécules suivantes : Hydrogène et Oxygéne, générez la molécule la plus courante et "
            "retournez les spécifications complètes de cette molécule au format JSON structuré.\n"
            "Le format attendu est :\n"
            "{\n"
            "    \"name\": \"Nom de la molécule\",\n"
            "    \"formula\": \"Formule chimique\",\n"
            "    \"components\": [\n"
            "        {\n"
            "            \"name\": \"Nom du composant\",\n"
            "            \"symbol\": \"Symbole du composant\",\n"
            "            \"atomic_number\": Numéro atomique,\n"
            "            \"atomic_mass\": Masse atomique,\n"
            "            \"category\": \"Catégorie de l'élément (ex: nonmetal, metal)\",\n"
            "            \"state\": \"État (ex: gas, liquid, solid)\"\n"
            "        },\n"
            "        ...\n"
            "    ],\n"
            "    \"state\": \"État de la molécule (ex: liquid, gas)\"\n"
            "}\n"
            "Veuillez renvoyer uniquement le JSON attendu sans texte supplémentaire ni balises de code ou backticks."
        ),
    }
]

try:
    chat_response = client.chat.complete(
        model=model,
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )
    response_text = chat_response.choices[0].message.content.strip()
    pattern = r'```json\s*(\{[\s\S]*?\})\s*```'
    match = re.search(pattern, response_text)
    if match:
        json_str = match.group(1)
    else:
        json_str = response_text.strip('`').strip()
    try:
        response_dict = json.loads(json_str)
        with open("response.json", "w", encoding='utf-8') as jsonfile:
            json.dump(response_dict, jsonfile, ensure_ascii=False, indent=4)
        print("Les données ont été enregistrées dans 'response.json' avec succès.")
    except json.JSONDecodeError as e:
        print("La réponse n'est pas au format JSON attendu :\n", response_text)
        print("Erreur de parsing JSON :", e)

except Exception as e:
    print(f"Une erreur s'est produite lors de la requête : {e}")
