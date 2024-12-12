import os
import json
import sys

ELEMENTS_FILE_PATH = "data/elements.json"

ELEMENTS_DATA = {
    "elements": [
        {"name": "Hydrogen", "symbol": "H", "atomic_number": 1, "atomic_mass": 1.008, "category": "nonmetal", "state": "gas"},
        {"name": "Helium", "symbol": "He", "atomic_number": 2, "atomic_mass": 4.0026, "category": "noble gas", "state": "gas"},
        {"name": "Carbon", "symbol": "C", "atomic_number": 6, "atomic_mass": 12.011, "category": "nonmetal", "state": "solid"},
        {"name": "Oxygen", "symbol": "O", "atomic_number": 8, "atomic_mass": 15.999, "category": "nonmetal", "state": "gas"}
    ]
}

def initialize_elements_file():
    """Initializes the elements file with predefined data if it doesn't exist."""
    try:
        if not os.path.exists(ELEMENTS_FILE_PATH):
            print(f"Fichier {ELEMENTS_FILE_PATH} introuvable. Création d'un nouveau fichier...")
            os.makedirs(os.path.dirname(ELEMENTS_FILE_PATH), exist_ok=True)
            with open(ELEMENTS_FILE_PATH, "w") as file:
                json.dump(ELEMENTS_DATA, file, indent=4)
            print("Fichier créé et initialisé avec les éléments de base.")
        else:
            print(f"Fichier {ELEMENTS_FILE_PATH} trouvé. Aucune action nécessaire.")
    except OSError as e:
        print(f"Erreur lors de la création du fichier {ELEMENTS_FILE_PATH}: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Erreur de format JSON lors de l'écriture des données dans le fichier {ELEMENTS_FILE_PATH}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")
        sys.exit(1)
