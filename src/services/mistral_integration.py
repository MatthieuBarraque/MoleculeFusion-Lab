from mistralai import Mistral
from dotenv import load_dotenv
import os
import json
import time
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
        details += f"Symbole: {element.get('symbol', 'Inconnu')}\n"
        details += f"Numéro atomique: {element.get('atomic_number', 'Inconnu')}\n"
        details += f"Masse atomique: {element.get('atomic_mass', 'Inconnu')}\n"
        details += f"Catégorie: {element.get('category', 'Inconnu')}\n"
        details += f"État: {element.get('state', 'Inconnu')}\n"
        return details

    def prepare_messages(self, elements_details):
        content = PROMPT_TEMPLATE.format(elements_details="\n".join(elements_details))
        return [{"role": "user", "content": content}]

    def send_request(self, messages, timeout=10):
        print("Request to Mistral started...")  
        start_time = time.time()
        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            if time.time() - start_time > timeout:
                print("Request to Mistral timed out.")
                raise TimeoutError("Request to Mistral timed out.")
            response_content = chat_response.choices[0].message.content.strip()
            print(f"Request to Mistral completed with response: {response_content}")
            return response_content
        except TimeoutError as e:
            print(f"Timeout error: {e}")
            return "Aucune réaction n'est possible entre ces éléments."
        except Exception as e:
            print(f"An error occurred during the request: {e}")
            return None

    def parse_response(self, response_text):
        print("Raw model response:", repr(response_text))
        response_text = response_text.strip().strip('`')  # Remove backticks
        if response_text.startswith('json'):
            response_text = response_text[4:].strip()  # Remove 'json' if present

        if "Aucune réaction n'est possible entre ces éléments." in response_text:
            return {'error': "Aucune réaction n'est possible entre ces éléments."}

        try:
            json_text = "[" + response_text.replace("}\n{", "},{") + "]"
            products = json.loads(json_text)
            return products
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
            return {'error': "Erreur de format JSON dans la réponse du modèle."}

    def create_element(self, *elements):
        elements_details = [self.format_element_details(elem) for elem in elements]
        messages = self.prepare_messages(elements_details)

        # Display animation during processing
        self.stop_animation = False
        animation_thread = Thread(target=animate_loading, args=("Création en cours", lambda: self.stop_animation))
        animation_thread.start()

        response_text = self.send_request(messages)
        self.stop_animation = True
        animation_thread.join()

        if response_text:
            parsed_response = self.parse_response(response_text)
            if isinstance(parsed_response, list):  # Check if we got a valid list of products
                return parsed_response
            elif 'error' in parsed_response:
                print(f"Error from model response: {parsed_response['error']}")
                return None
        else:
            print("Empty response or error in request.")
            return None

