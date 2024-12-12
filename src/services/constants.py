# src/services/constants.py

MODEL_NAME = "mistral-large-latest"

PROMPT_TEMPLATE = (
    "En combinant les éléments ou composés suivants, déterminez s'il existe une réaction chimique connue entre eux. "
    "Fournissez les spécifications complètes des produits de cette réaction au format JSON structuré, sans texte supplémentaire. "
    "Si aucune réaction n'est possible, renvoyez uniquement : \"Aucune réaction n'est possible entre ces éléments.\"\n\n"
    "Éléments à combiner:\n"
    "{elements_details}\n"
    "Le format attendu pour chaque produit est :\n"
    '{{"name": "Nom du produit", "formula": "Formule chimique", "components": [{{"name": "Nom du composant", "symbol": "Symbole du composant"}}], "state": "État du produit"}}\n'
    "Si plusieurs produits sont formés, renvoyez chaque objet JSON sur une seule ligne.\n"
    "Répondez uniquement avec le ou les objets JSON attendus, sans balises de code ou texte additionnel."
)
