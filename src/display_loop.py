# src/display_loop.py
from services.load_elements import load_elements
from services.mistral_integration import MistralIntegration
import os
import json
import traceback

def display_elements():
    """Affiche les noms des éléments et gère l'interaction utilisateur."""
    base_elements = load_elements()
    if not base_elements:
        print("Aucun élément trouvé.")
        return

    # Charger les éléments créés s'ils existent
    created_elements = []
    created_elements_path = os.path.join("data", "created_elements.json")
    if os.path.exists(created_elements_path):
        with open(created_elements_path, "r", encoding='utf-8') as f:
            created_elements = json.load(f)

    mistral_integration = MistralIntegration()

    while True:
        # Affichage des éléments disponibles
        all_elements = base_elements + created_elements
        print("\n--- Liste des éléments disponibles ---\n")
        for idx, element in enumerate(all_elements, start=1):
            print(f"{idx}. {element.get('name', 'Nom inconnu')}")

        # Afficher les éléments créés s'il y en a
        if created_elements:
            print("\n--- Élément(s) créé(s) ---")
            for element in created_elements:
                print(f"- {element.get('name', 'Nom inconnu')} ({element.get('formula', 'Formule inconnue')})")

        # Options d'interaction utilisateur
        print("\nOptions:")
        print(" - Entrez 'c' pour créer un nouvel élément.")
        print(" - Entrez 'q' pour quitter.")
        print(" - Appuyez sur Entrée pour rafraîchir la liste.\n")
        user_input = input("> ").strip().lower()

        if user_input == 'q':
            print("Arrêt du programme.")
            break
        elif user_input == 'c':
            # Sélection des éléments à fusionner avec validation
            try:
                idx1 = int(input("Entrez le numéro du premier élément à fusionner: ").strip()) - 1
                idx2 = int(input("Entrez le numéro du second élément à fusionner: ").strip()) - 1
                if idx1 < 0 or idx2 < 0 or idx1 >= len(all_elements) or idx2 >= len(all_elements):
                    print("Numéros d'éléments invalides. Veuillez réessayer.")
                    continue
                element1, element2 = all_elements[idx1], all_elements[idx2]
            except ValueError:
                print("Erreur : Veuillez entrer des numéros valides pour les éléments.")
                continue
            except IndexError:
                print("Erreur : Numéro d'élément hors de portée.")
                continue

            # Création de l'élément
            print("Création de l'élément en cours, veuillez patienter...\n")
            result = mistral_integration.create_element(element1, element2)

            if result is None:
                print("La création de l'élément a échoué. Veuillez réessayer.")
            elif isinstance(result, dict) and 'error' in result:
                # Le modèle a renvoyé un message d'erreur
                print(f"Erreur : {result['error']}")
            elif isinstance(result, list):
                for created_element in result:
                    # Validation de l'élément créé
                    if isinstance(created_element, dict) and 'name' in created_element and 'formula' in created_element:
                        try:
                            # Vérification de l'existence de l'élément
                            element_exists = any(
                                elem.get('name') == created_element.get('name') and
                                elem.get('formula') == created_element.get('formula')
                                for elem in created_elements
                            )
                            if element_exists:
                                print(f"L'élément {created_element.get('name', 'Inconnu')} a déjà été créé précédemment.")
                            else:
                                # Ajout et sauvegarde de l'élément créé
                                created_elements.append(created_element)
                                with open(created_elements_path, "w", encoding='utf-8') as f:
                                    json.dump(created_elements, f, ensure_ascii=False, indent=4)
                                print(f"Nouvel élément créé avec succès : {created_element.get('name', 'Inconnu')} ({created_element.get('formula', 'Formule inconnue')})")
                        except Exception as e:
                            print(f"Une erreur s'est produite lors du traitement de l'élément créé : {e}")
                            traceback.print_exc()
                    else:
                        print("L'un des éléments créés n'est pas valide et ne sera pas ajouté.")
            else:
                print("Une erreur inattendue s'est produite. Veuillez réessayer.")
        elif user_input == '':
            continue
        else:
            print("Option non reconnue. Veuillez entrer 'c', 'q', ou appuyer sur Entrée.")

if __name__ == "__main__":
    try:
        display_elements()
    except Exception as e:
        print("Erreur lors de l'exécution du programme :")
        traceback.print_exc()
