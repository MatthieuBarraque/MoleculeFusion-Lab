# src/mistral_integration.py
from mistralai import Mistral
from dotenv import load_dotenv
import os
import json
import re
from threading import Thread
from .animation import animate_loading
from .constants import MODEL_NAME, PROMPT_TEMPLATE

class MistralIntegration:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API MISTRAL_API_KEY est manquante dans les variables d'environnement.")
        self.client = Mistral(api_key=self.api_key)
        self.model = MODEL_NAME
        self.stop_animation = False

    def format_element_details(self, element):
        details = f"Nom: {element.get('name', 'Inconnu')}\n"
        if 'formula' in element:
            details += f"Formule: {element.get('formula', 'Inconnue')}\n"
            details += "Composants:\n"
            for comp in element.get('components', []):
                details += f" - {comp.get('name', 'Inconnu')} ({comp.get('symbol', 'Inconnu')})\n"
        else:
            details += f"Symbole: {element.get('symbol', 'Inconnu')}\n"
            details += f"Numéro atomique: {element.get('atomic_number', 'Inconnu')}\n"
            details += f"Masse atomique: {element.get('atomic_mass', 'Inconnu')}\n"
            details += f"Catégorie: {element.get('category', 'Inconnue')}\n"
            details += f"État: {element.get('state', 'Inconnu')}\n"
        return details

    def prepare_messages(self, element1_details, element2_details):
        content = PROMPT_TEMPLATE.format(
            element1_details=element1_details,
            element2_details=element2_details
        )
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        return messages

    def send_request(self, messages):
        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return chat_response.choices[0].message.content.strip()
        except Exception as e:
            print(f"\nUne erreur s'est produite lors de la requête : {e}")
            return None

    def parse_response(self, response_text):
        print("Réponse brute du modèle :", repr(response_text))
        response_text = response_text.strip().strip('`')
        if response_text.startswith('json'):
            response_text = response_text[4:].strip()
        if "Aucune réaction n'est possible entre ces éléments." in response_text:
            print("Le modèle a indiqué qu'aucune réaction n'est possible.")
            return {'error': "Aucune réaction n'est possible entre ces éléments."}
        if not response_text.startswith('{') and not response_text.startswith('['):
            print("Le modèle a renvoyé un message d'erreur ou aucune réaction n'est possible.")
            return {'error': response_text}
        try:
            json_text = "[" + response_text.replace("}\n{", "},{") + "]"
            products = json.loads(json_text)
            return products
        except json.JSONDecodeError as e:
            print("Erreur lors du parsing du JSON :", e)
            json_objects = []
            json_strs = re.findall(r'\{(?:[^{}]|(?R))*\}', response_text, re.MULTILINE | re.DOTALL)
            for json_str in json_strs:
                try:
                    json_obj = json.loads(json_str)
                    json_objects.append(json_obj)
                except json.JSONDecodeError:
                    continue
            if json_objects:
                return json_objects
            else:
                print("Impossible de parser les objets JSON.")
                return {'error': "La réponse du modèle ne contient pas de produit valide."}


    def create_element(self, element1, element2):
        """Crée un nouvel élément en fusionnant deux éléments existants."""
        # Trier les éléments par nom pour assurer la cohérence
        elements = sorted([element1, element2], key=lambda e: e.get('name', ''))
        element1_sorted = elements[0]
        element2_sorted = elements[1]
        element1_details = self.format_element_details(element1_sorted)
        element2_details = self.format_element_details(element2_sorted)
        messages = self.prepare_messages(element1_details, element2_details)
        animation_thread = Thread(target=animate_loading, args=("Création en cours", lambda: self.stop_animation))
        animation_thread.start()
        response_text = self.send_request(messages)
        self.stop_animation = True
        animation_thread.join()

        if response_text:
            return self.parse_response(response_text)
        else:
            return None
