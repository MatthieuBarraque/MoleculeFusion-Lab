from gui.drag_drop_handler import DraggableElement
from services.load_elements import save_created_element
import math

def create_canvas_element(app, element, x, y, merged=False):
    """Crée un élément déplaçable sur le canvas avec un centrage correct."""
    style = 'CreatedElement.TLabel' if merged else 'Element.TLabel'
    element_label = DraggableElement(
        app.center_canvas, element, app, is_canvas=True,
        element_data=element, style=style
    )
    window_id = app.center_canvas.create_window(x, y, window=element_label, anchor="center")
    element_label.set_window_id(window_id)
    app.center_elements.append(element_label)
    print(f"Élément '{element['name']}' ajouté au canvas central à ({x}, {y}).")

    if merged:
        # Sauvegarder l'élément fusionné
        save_created_element(element)
        # Ajouter à la liste des éléments créés dans le GUI
        app.add_created_element_to_gui(element)

def is_overlapping(elem1, elem2, threshold=100):
    """Vérifie si deux éléments sur le canvas se chevauchent."""
    x1, y1 = elem1.get_position()
    x2, y2 = elem2.get_position()
    distance = math.hypot(x1 - x2, y1 - y2)
    print(f"Distance entre '{elem1.name}' et '{elem2.name}' : {distance}")
    return distance < threshold

def check_all_mergings(app):
    """Détecte et fusionne les éléments qui se chevauchent sur le canvas."""
    merged_elements = set()
    combinations = []

    for i, elem1 in enumerate(app.center_elements):
        for elem2 in app.center_elements[i+1:]:
            if elem1 in merged_elements or elem2 in merged_elements:
                continue
            if is_overlapping(elem1, elem2):
                combined_components = elem1.element_data.get("components", []) + elem2.element_data.get("components", [])
                combination_text = f"{elem1.name} + {elem2.name}"
                combinations.append((elem1, elem2, combination_text, combined_components))
                merged_elements.update([elem1, elem2])
                print(f"Combinaison trouvée : '{elem1.name}' + '{elem2.name}'")

    for elem1, elem2, combo_text, combined_components in combinations:
        # Supprimer les deux éléments du canvas
        try:
            app.center_canvas.delete(elem1.window_id)
            app.center_canvas.delete(elem2.window_id)
            app.center_elements.remove(elem1)
            app.center_elements.remove(elem2)
            print(f"Éléments '{elem1.name}' et '{elem2.name}' supprimés du canvas.")
        except Exception as e:
            print(f"Erreur lors de la suppression des éléments : {e}")

        # Calculer la nouvelle position au centre des deux éléments
        x1, y1 = elem1.get_position()
        x2, y2 = elem2.get_position()
        merged_x = (x1 + x2) / 2
        merged_y = (y1 + y2) / 2

        # Créer le nouvel élément fusionné
        new_element = {
            "name": combo_text,
            "formula": "",  # Optionnel : générer la formule
            "components": combined_components,
            "state": "unknown"  # Optionnel : déterminer l'état
        }
        create_canvas_element(app, new_element, merged_x, merged_y, merged=True)
        print(f"Élément fusionné '{combo_text}' créé à ({merged_x}, {merged_y}).")

        # Mettre à jour l'étiquette de combinaison
        app.combination_text = [elem.name for elem in app.center_elements]
        app.update_combination_label()
