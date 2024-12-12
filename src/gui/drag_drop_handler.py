import tkinter as tk
from tkinter import ttk

class DraggableElement(ttk.Label):
    """Représente un élément déplaçable dans l'interface."""
    def __init__(self, master, element, app, is_canvas=False, element_data=None, merged=False, style=None):
        if not isinstance(element, dict):
            print(f"Type d'élément incorrect : {type(element)}. Élément reçu : {element}")
            raise TypeError("L'élément doit être un dictionnaire avec les clés 'name', 'formula', etc.")
        
        name = element["name"]
        formula = element.get("formula", "")
        display_text = f"{name} ({formula})" if formula else name

        super().__init__(master, text=display_text, style=style)

        self.master = master  # Peut être un cadre défilant ou un canvas
        self.name = name
        self.formula = formula
        self.app = app
        self.is_canvas = is_canvas
        self.merged = merged  # Indique si l'élément est fusionné
        self.selected = False  # Indicateur de sélection

        # Stockage des données de l'élément
        self.element_data = element_data or {
            "name": name,
            "formula": formula,
            "components": element.get("components", []),
            "state": element.get("state", "")
        }

        # Liaison des événements de souris
        self.bind("<ButtonPress-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)

        # Données de déplacement
        self.drag_data = {"x": 0, "y": 0}

        # Pour les éléments sur le canvas, stocker window_id
        self.window_id = None

    def toggle_selection(self):
        """Toggle the selection state of the element."""
        self.selected = not self.selected
        if self.selected:
            self.config(relief="sunken", background="#ADD8E6")
            print(f"Élément '{self.name}' sélectionné.")
        else:
            self.config(relief="raised", background="#FFFFFF")
            print(f"Élément '{self.name}' désélectionné.")

    def on_start_drag(self, event):
        """Initialise les données de déplacement et gère la sélection."""
        if not self.is_canvas and self.merged:
            # Ne pas permettre de drag des éléments fusionnés depuis les listes
            print(f"Drag non autorisé pour l'élément fusionné : {self.name}")
            return

        # Toggle selection directement ici
        self.toggle_selection()

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        if self.is_canvas and self.window_id:
            self.lift()
        else:
            # Créer un élément flottant qui suit le curseur
            self.app.start_floating_drag(self.element_data["name"], event)
            print(f"Drag commencé pour l'élément '{self.name}'.")

    def on_drag(self, event):
        """Gère le déplacement de l'élément."""
        if self.is_canvas and self.window_id:
            # Déplacer l'élément sur le canvas
            try:
                # Obtenir les coordonnées actuelles de l'élément
                coords = self.master.coords(self.window_id)
                if len(coords) >= 2:
                    x, y = coords[:2]
                    # Calculer le déplacement par rapport au point de départ
                    dx = event.x - self.drag_data["x"]
                    dy = event.y - self.drag_data["y"]
                    # Appliquer le déplacement
                    self.master.coords(self.window_id, x + dx, y + dy)
                    # Vérifier les fusions en temps réel
                    self.app.check_all_mergings()
                    print(f"Élément '{self.name}' déplacé sur le canvas à ({x + dx}, {y + dy}).")
            except Exception as e:
                print(f"Erreur lors du déplacement de {self.name} sur le canvas : {e}")
        else:
            # Mettre à jour la position de l'élément flottant
            if self.app.floating_drag:
                self.app.update_floating_drag(event)
                print(f"Élément flottant '{self.name}' déplacé à ({self.app.floating_drag.winfo_x()}, {self.app.floating_drag.winfo_y()}).")
            else:
                print(f"Élément flottant '{self.name}' tenté de déplacer, mais floating_drag est None.")

    def on_drop(self, event):
        """Gère l'événement de lâcher de l'élément."""
        if self.is_canvas and self.window_id:
            # Vérifier les fusions après le déplacement
            self.app.check_all_mergings()
            print(f"Élément '{self.name}' lâché sur le canvas.")
        else:
            # Finaliser le drag flottant
            self.app.finalize_floating_drag(event, self.element_data["name"])
            print(f"Élément flottant '{self.name}' finalisé.")

    def set_window_id(self, window_id):
        """Assigne l'ID de la fenêtre du canvas à l'élément."""
        self.window_id = window_id

    def get_position(self):
        """Retourne la position centrale de l'élément sur le canvas."""
        if self.is_canvas and self.window_id:
            coords = self.master.coords(self.window_id)
            if len(coords) >= 2:
                x, y = coords[:2]
                # To get the central position, add half of the widget's width and height
                self.update_idletasks()  # Ensure width and height are updated
                width = self.winfo_width()
                height = self.winfo_height()
                return x + width / 2, y + height / 2
            else:
                return 0, 0
        else:
            return self.winfo_x(), self.winfo_y()
