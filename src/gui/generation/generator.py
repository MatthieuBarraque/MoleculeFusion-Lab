from threading import Thread
from tkinter import messagebox
from services.mistral_integration import MistralIntegration
from .prompt_manager import generate_prompt
from services.load_elements import save_created_element
import json

class Generator:
    def __init__(self, app):
        self.app = app
        self.mistral = MistralIntegration()
    
    def format_element_details(self, elements):
        """Formate les détails des éléments pour le prompt."""
        details = ""
        for idx, element in enumerate(elements, start=1):
            details += f"Élément {idx}:\n"
            if 'formula' in element and element['formula']:
                details += f"Nom: {element.get('name', 'Inconnu')}\n"
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
            details += "\n"
        print(f"Détails des éléments formatés :\n{details}")
        return details
    
    def generate_elements(self, selected_elements):
        """Génère de nouveaux éléments en combinant les éléments sélectionnés."""
        if not selected_elements:
            messagebox.showwarning("Avertissement", "Aucun élément sélectionné pour la fusion.")
            return
        
        elements_details = self.format_element_details(selected_elements)
        prompt = generate_prompt(elements_details)
        print(f"Prompt généré pour Mistral :\n{prompt}")
    
        def task():
            try:
                self.app.animate_loading("Génération en cours...")
                print("Envoi de la requête à Mistral.")
                response = self.mistral.send_request(self.mistral.prepare_messages(prompt))
                self.app.stop_animation()
                print(f"Réponse reçue de Mistral :\n{response}")
    
                if not response:
                    messagebox.showerror("Erreur", "Échec de la génération des nouveaux éléments.")
                    return
    
                products = self.mistral.parse_response(response)
                print(f"Produits analysés :\n{products}")
    
                if isinstance(products, dict) and 'error' in products:
                    messagebox.showerror("Erreur", products['error'])
                    return
                elif isinstance(products, list):
                    new_elements = []
                    for product in products:
                        if isinstance(product, dict) and 'name' in product and 'formula' in product:
                            # Vérifier si l'élément existe déjà
                            exists = any(
                                elem.get('name') == product.get('name') and
                                elem.get('formula') == product.get('formula')
                                for elem in self.app.created_elements
                            )
                            if exists:
                                print(f"Élément '{product.get('name')}' existe déjà. Ignoré.")
                                continue
                            else:
                                new_elements.append(product)
                                save_created_element(product)
                                self.app.add_created_element_to_gui(product)
                                print(f"Nouvel élément '{product.get('name')}' créé et ajouté au GUI.")
                    if new_elements:
                        messagebox.showinfo("Succès", f"{len(new_elements)} nouvel(s) élément(s) créé(s) avec succès.")
                        print(f"{len(new_elements)} nouvel(s) élément(s) créé(s) avec succès.")
                    else:
                        messagebox.showinfo("Info", "Aucun nouvel élément n'a été créé.")
                        print("Aucun nouvel élément n'a été créé.")
                else:
                    messagebox.showerror("Erreur", "Format de réponse inattendu de Mistral.")
                    print("Format de réponse inattendu.")
            except Exception as e:
                self.app.stop_animation()
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
                print(f"Exception lors de la génération d'éléments : {e}")
    
        Thread(target=task).start()
