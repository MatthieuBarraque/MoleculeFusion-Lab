PROMPT_TEMPLATE = (
    "En combinant les éléments ou composés suivants, déterminez s'il existe une réaction chimique connue entre eux. "
    "Considérez les éléments de manière non ordonnée, c'est-à-dire que l'ordre n'a pas d'importance. "
    "Si une réaction est possible, fournissez les spécifications complètes des produits de cette réaction au format JSON structuré, sans texte supplémentaire, "
    "et en veillant à ce que chaque objet JSON soit sur une seule ligne, sans indentations ni sauts de ligne. "
    "Si aucune réaction n'est possible, veuillez renvoyer le message suivant exactement comme écrit : "
    "\"Aucune réaction n'est possible entre ces éléments.\"\n\n"
    "Éléments à combiner:\n"
    "{elements_details}\n"
    "Le format attendu pour chaque produit est exactement ceci (remplacez les valeurs par les vôtres) :\n"
    '{{"name": "Nom du produit", "formula": "Formule chimique", "components": [{{"name": "Nom du composant", "symbol": "Symbole du composant", "atomic_number": Numéro atomique, "atomic_mass": Masse atomique, "category": "Catégorie de l\'élément", "state": "État"}}], "state": "État du produit"}}\n'
    "Si plusieurs produits sont formés, renvoyez chaque objet JSON sur une seule ligne, séparé par une nouvelle ligne, sans texte supplémentaire.\n"
    "Veuillez renvoyer uniquement le ou les objets JSON attendus, sans texte supplémentaire, sans balises de code ou backticks."
)

def generate_prompt(elements_details):
    """Génère un prompt pour Mistral basé sur les détails des éléments."""
    prompt = PROMPT_TEMPLATE.format(elements_details=elements_details)
    print(f"Prompt généré pour Mistral :\n{prompt}")
    return prompt
