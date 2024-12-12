# src/gui/app.py
import tkinter as tk
from tkinter import ttk, messagebox
from gui.drag_drop_handler import DraggableElement
from services.load_elements import load_elements, load_created_elements, save_created_element
from services.mistral_integration import MistralIntegration
from gui.styles import setup_styles
from gui.layout import setup_layout
from gui.canvas_manager import create_canvas_element, check_all_mergings
from services.animation import animate_loading
import json
import os
import threading


class ElementApp:
    def __init__(self, elements, created_elements):
        self.elements = elements
        self.created_elements = created_elements
        self.center_elements = []
        self.floating_drag = None
        self.combination_text = []

        # Initialize Mistral Integration
        try:
            self.mistral = MistralIntegration()
        except ValueError as ve:
            messagebox.showerror("Erreur de configuration", str(ve))
            raise

        # Configuration of main window
        self.root = tk.Tk()
        self.root.title("Element Combiner")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Combination status label
        self.status_label = ttk.Label(self.root, text="Status: Ready", style='Status.TLabel')
        self.status_label.pack(anchor="n", pady=(10, 0))  # Positioned at the top with padding

        # Other GUI setup
        setup_styles()
        setup_layout(self)

    def on_center_resize(self, event):
        """Recentre l'étiquette de combinaison lors du redimensionnement."""
        if hasattr(self, 'center_canvas') and hasattr(self, 'combination_window'):
            new_x = event.width / 2
            self.center_canvas.coords(self.combination_window, new_x, 20)
            print(f"Canvas redimensionné, combinaison étiquette recentrée à ({new_x}, 20).")

    def create_canvas_element(self, element, x, y, merged=False):
        """Crée et affiche un élément déplaçable sur le canvas central."""
        print(f"Création de l'élément sur le canvas : {element} à ({x}, {y})")
        create_canvas_element(self, element, x, y, merged)

        # Ajouter le nom de l'élément au texte de combinaison s'il est unique
        if element['name'] not in self.combination_text:
            self.combination_text.append(element['name'])
            self.update_combination_label()

    def update_combination_label(self):
        """Met à jour l'étiquette de combinaison avec la combinaison actuelle."""
        if self.combination_text:
            self.combination_label.config(text=" + ".join(self.combination_text))
        else:
            self.combination_label.config(text="")

    def combine_elements(self):
        """Combine selected elements on the canvas using a background thread."""
        selected_elements = self.get_selected_elements()
        element_names = [elem.name for elem in selected_elements]
        print(f"Tentative de fusion des éléments : {element_names}")

        if len(selected_elements) < 2:
            messagebox.showwarning("Avertissement", "Sélectionnez au moins deux éléments pour la fusion.")
            return

        elements_data = [elem.element_data for elem in selected_elements]
        self.status_label.config(text="Status: Processing...")

        # Run the Mistral request in a background thread
        thread = threading.Thread(target=self.handle_mistral_request, args=(elements_data,))
        thread.start()

    def handle_mistral_request(self, elements_data):
        """Handle the Mistral request in a separate thread."""
        response = self.mistral.create_element(*elements_data)

        # Process the response on the main thread
        self.root.after(0, self.process_mistral_response, response)

    def process_mistral_response(self, response):
        if response is None:
            self.status_label.config(text="Status: Error in generation")
            messagebox.showerror("Erreur", "La génération du nouvel élément a échoué.")
            return

        if isinstance(response, dict) and 'error' in response:
            self.status_label.config(text="Status: No reaction possible")
            messagebox.showwarning("Avertissement", response['error'])
            return

        for product in response:
            print(f"Nouveau produit généré par Mistral : {product}")
            positions = [elem.get_position() for elem in self.get_selected_elements()]
            avg_x = sum(pos[0] for pos in positions) / len(positions)
            avg_y = sum(pos[1] for pos in positions) / len(positions)

            # Create the new element on the canvas and save it
            self.create_canvas_element(product, avg_x, avg_y, merged=True)
            save_created_element(product)
            self.add_created_element_to_gui(product)

        # Clear selection and update status
        self.combination_text = []
        self.update_combination_label()
        self.status_label.config(text="Status: Fusion successful")
        messagebox.showinfo("Succès", "Les éléments ont été fusionnés et le nouvel élément a été généré.")


    def clear_canvas(self):
        """Supprime tous les éléments du canvas central et du fichier created_elements.json."""
        for elem in self.center_elements:
            try:
                self.center_canvas.delete(elem.window_id)
            except Exception as e:
                print(f"Erreur lors de la suppression de l'élément '{elem.name}' : {e}")
        self.center_elements.clear()
        self.created_elements = []
        #self.save_created_elements()
        self.combination_text = []
        self.update_combination_label()
        print("Canvas et created_elements.json ont été réinitialisés.")


    def save_created_elements(self):
        """Sauvegarde les éléments créés dans created_elements.json."""
        with open('data/created_elements.json', 'w', encoding='utf-8') as f:
            json.dump(self.created_elements, f, ensure_ascii=False, indent=4)
        print("created_elements.json a été sauvegardé.")

    def add_created_element_to_gui(self, element):
        """Ajoute un nouvel élément créé à la liste des éléments créés dans le GUI."""
        if hasattr(self, 'created_scrollable_frame') and self.created_scrollable_frame:
            # Vérifier si l'élément existe déjà
            for child in self.created_scrollable_frame.winfo_children():
                if isinstance(child, DraggableElement) and child.name == element['name']:
                    print(f"L'élément '{element['name']}' existe déjà dans les éléments créés.")
                    return
            # Créer et ajouter le nouvel élément
            element_label = DraggableElement(
                self.created_scrollable_frame, element, self,
                is_canvas=False, element_data=element, merged=True, style='CreatedElement.TLabel'
            )
            element_label.pack(anchor="w", padx=10, pady=5, fill='x')
            print(f"Élément '{element['name']}' ajouté à la liste des éléments créés dans le GUI.")

    def get_selected_elements(self):
        """Récupère les éléments sélectionnés sur le canvas central."""
        return [elem for elem in self.center_elements if elem.selected]

    def run(self):
        """Lance la boucle principale de l'application."""
        print("Lancement de la boucle principale de l'application.")

        # Ajouter un élément de test pour vérifier l'affichage du canvas
        #test_element = {
        #    "name": "TestElement",
        #    "formula": "TE",
        #    "components": [],
        #    "state": "solid"
        #}
        #self.create_canvas_element(test_element, 600, 100)  # Positionné au centre supérieur
        #print("Élément de test ajouté au canvas.")

        self.root.mainloop()

    def check_all_mergings(self):
        """Méthode pour vérifier toutes les fusions sur le canvas."""
        check_all_mergings(self)

    # Ajout des fonctions de drag flottant
    def start_floating_drag(self, element_name, event):
        """Crée un élément flottant qui suit le curseur pendant le drag."""
        if self.floating_drag:
            self.floating_drag.destroy()

        self.floating_drag = tk.Toplevel(self.root)
        self.floating_drag.overrideredirect(True)  # Supprimer la bordure
        self.floating_drag.attributes("-alpha", 0.7)  # Semi-transparent

        label = ttk.Label(self.floating_drag, text=element_name, style='Element.TLabel')
        label.pack()

        # Position initiale du flottant
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        self.floating_drag.geometry(f"+{x}+{y}")

    def update_floating_drag(self, event):
        """Met à jour la position de l'élément flottant."""
        if self.floating_drag:
            x = event.x_root - self.root.winfo_rootx()
            y = event.y_root - self.root.winfo_rooty()
            self.floating_drag.geometry(f"+{x}+{y}")

    def finalize_floating_drag(self, event, element_name):
        """Finalise le drag flottant et ajoute l'élément au canvas."""
        if self.floating_drag:
            # Calculer les coordonnées relatives au canvas
            canvas_x = self.center_canvas.winfo_pointerx() - self.center_canvas.winfo_rootx()
            canvas_y = self.center_canvas.winfo_pointery() - self.center_canvas.winfo_rooty()

            # Trouver l'élément correspondant
            element = next((elem for elem in self.elements if elem["name"] == element_name), None)
            if element:
                self.create_canvas_element(element, canvas_x, canvas_y)
            else:
                messagebox.showerror("Erreur", f"L'élément '{element_name}' n'existe pas.")

            self.floating_drag.destroy()
            self.floating_drag = None
