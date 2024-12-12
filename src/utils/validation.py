def validate_unique_elements(element_name, selected_elements):
    """Assure que l'élément n'est pas déjà sélectionné."""
    if element_name in selected_elements:
        print(f"Erreur: {element_name} est déjà sélectionné.")
        return False
    return True
