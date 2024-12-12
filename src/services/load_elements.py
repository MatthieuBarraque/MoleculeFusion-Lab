# src/services/load_elements.py
import json
import os

def load_elements(filepath):
    """Charge les éléments depuis le fichier JSON spécifié."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Le fichier {filepath} n'existe pas.")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ajout d'une impression pour vérifier le contenu
    print(f"Contenu chargé depuis {filepath} : {data}")
    
    # Extraire la liste des éléments
    if "elements" not in data:
        raise ValueError("Le fichier JSON doit contenir une clé 'elements' avec une liste d'éléments.")
    
    elements = data["elements"]
    
    # Vérification du format des éléments
    if not isinstance(elements, list):
        raise ValueError("La valeur de 'elements' dans le fichier JSON doit être une liste.")
    for elem in elements:
        if not isinstance(elem, dict):
            raise ValueError("Chaque élément dans la liste 'elements' doit être un dictionnaire.")
        required_keys = {"name", "symbol", "atomic_number", "atomic_mass", "category", "state"}
        if not required_keys.issubset(elem.keys()):
            raise ValueError(f"L'élément {elem} manque des clés requises : {required_keys}")
    
    print(f"Nombre d'éléments chargés : {len(elements)}")
    return elements

def load_created_elements(filepath):
    """Charge les éléments créés depuis le fichier JSON spécifié."""
    if not os.path.exists(filepath):
        # Si le fichier n'existe pas, créer une liste vide
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        created_elements = json.load(f)
    
    # Ajout d'une impression pour vérifier le contenu
    print(f"Contenu chargé depuis {filepath} : {created_elements}")
    
    # Vérification du format des éléments créés
    if not isinstance(created_elements, list):
        raise ValueError("Le fichier JSON des éléments créés doit contenir une liste d'éléments.")
    for elem in created_elements:
        if not isinstance(elem, dict):
            raise ValueError("Chaque élément créé dans le fichier JSON doit être un dictionnaire.")
        required_keys = {"name", "formula", "components", "state"}
        if not required_keys.issubset(elem.keys()):
            raise ValueError(f"L'élément créé {elem} manque des clés requises : {required_keys}")
    
    print(f"Nombre d'éléments créés chargés : {len(created_elements)}")
    return created_elements

def save_created_element(element):
    """Save a new created element to created_elements.json, ensuring no duplicates."""
    element['name'] = element['name'].replace("+", "").strip()  # Clean up name
    with open('data/created_elements.json', 'r+', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        # Avoid duplicates
        if element not in data:
            data.append(element)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Élément '{element['name']}' sauvegardé dans created_elements.json.")


