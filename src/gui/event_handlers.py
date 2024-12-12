from tkinter import messagebox
import os
import json

def clear_canvas(app):
    """Gère l'action de suppression du canvas."""
    confirm = messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir vider le canvas ?")
    if confirm:
        # Supprimer tous les éléments du canvas
        for elem in app.center_elements.copy():
            app.center_canvas.delete(elem.window_id)
            app.center_elements.remove(elem)
            print(f"Élément '{elem.name}' supprimé du canvas.")
        # Réinitialiser le texte de combinaison
        app.combination_text = []
        app.update_combination_label()
        
        # Vider created_elements.json
        try:
            with open(os.path.join('data', 'created_elements.json'), 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)
            app.created_elements = []
            # Vider la liste des éléments créés dans le GUI
            for child in app.created_scrollable_frame.winfo_children():
                child.destroy()
            print("Canvas et éléments créés vidés.")
        except Exception as e:
            print(f"Erreur lors de la suppression du canvas : {e}")
            messagebox.showerror("Erreur", f"Impossible de vider le canvas : {e}")
