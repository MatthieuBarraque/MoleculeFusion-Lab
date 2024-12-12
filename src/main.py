import os
import json
import sys
from  error.check_json_elements import initialize_elements_file
from display_loop import display_elements

from services.load_elements import load_elements, load_created_elements
from gui.app import ElementApp

def main():

    #print("\nInitialisation")
    #initialize_elements_file()
    #print("initialisé avec succès.")
    #display_elements()

    print("Initialisation")
    elements = load_elements('data/elements.json')
    print("Éléments chargés avec succès depuis elements.json.")
    created_elements = load_created_elements('data/created_elements.json')
    print("Éléments créés chargés avec succès depuis created_elements.json.")
    print("Initialisé avec succès.")

    app = ElementApp(elements, created_elements)
    print("Lancement de la boucle principale de l'application.")
    app.run()

if __name__ == "__main__":
    main()