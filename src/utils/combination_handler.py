
def handle_combination(element_names):
    """Génère le nom de la combinaison à partir des noms des éléments."""
    unique_elements = list(dict.fromkeys(element_names)) 
    combination = " + ".join(unique_elements)
    return combination
