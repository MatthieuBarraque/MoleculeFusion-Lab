import sys

def handle_file_not_found(file_path):
    """Gère l'erreur lorsque le fichier JSON est introuvable."""
    print(f"Erreur : Le fichier '{file_path}' est introuvable. Assurez-vous que le fichier existe.")
    sys.exit(1)

def handle_json_decode_error(file_path):
    """Gère l'erreur de décodage JSON."""
    print(f"Erreur : Le fichier '{file_path}' contient un format JSON invalide. Vérifiez le contenu du fichier.")
    sys.exit(1)
