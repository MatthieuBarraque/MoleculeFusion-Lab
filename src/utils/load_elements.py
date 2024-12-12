import json
import os

def load_elements(filepath):
    """Charge les éléments depuis le fichier JSON spécifié."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Le fichier {filepath} n'existe pas.")
    with open(filepath, 'r', encoding='utf-8') as f:
        elements = json.load(f)
    
    if not isinstance(elements, list):
        raise ValueError("Le fichier JSON des éléments doit contenir une liste d'éléments.")
    for elem in elements:
        if not isinstance(elem, dict):
            raise ValueError("Chaque élément dans le fichier JSON doit être un dictionnaire.")
        required_keys = {"name", "formula", "components", "state"}
        if not required_keys.issubset(elem.keys()):
            raise ValueError(f"L'élément {elem} manque des clés requises : {required_keys}")
    
    print(f"Nombre d'éléments chargés : {len(elements)}")
    return elements

def load_created_elements(filepath):
    """Charge les éléments créés depuis le fichier JSON spécifié."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        created_elements = json.load(f)
    
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

def save_created_element(element, filepath='data/created_elements.json'):
    """Sauvegarde un élément créé dans le fichier JSON spécifié."""
    if not os.path.exists(filepath):
        created_elements = []
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            created_elements = json.load(f)
    
    for existing in created_elements:
        if existing['name'] == element['name']:
            print(f"L'élément '{element['name']}' existe déjà dans created_elements.json.")
            return
    created_elements.append(element)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(created_elements, f, ensure_ascii=False, indent=4)
    print(f"L'élément '{element['name']}' a été sauvegardé dans created_elements.json.")
