import tkinter as tk
from tkinter import ttk
from gui.drag_drop_handler import DraggableElement

def setup_layout(app):
    """Configure la disposition des widgets dans la fenêtre."""
    paned_window = ttk.PanedWindow(app.root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Pane gauche (canvas)
    left_frame = ttk.Frame(paned_window, width=900, relief="sunken")
    paned_window.add(left_frame, weight=3)

    # Pane droite (listes d'éléments)
    right_frame = ttk.Frame(paned_window, width=300, relief="sunken")
    paned_window.add(right_frame, weight=1)

    # Canvas central
    app.center_canvas = tk.Canvas(left_frame, bg="#f0f0f0")
    app.center_canvas.pack(fill="both", expand=True, padx=10, pady=10)
    app.center_canvas.bind("<Configure>", app.on_center_resize)

    # Étiquette de combinaison en haut du canvas
    app.combination_label = ttk.Label(app.center_canvas, text="", style='Fusion.TLabel')
    app.combination_window = app.center_canvas.create_window(
        600, 20,  # Position initiale au centre supérieur
        window=app.combination_label, anchor="n"
    )

    # Configuration de la liste des éléments sur la droite
    ttk.Label(right_frame, text="Éléments", font=('Segoe UI', 14, 'bold')).pack(pady=(10, 5))
    elements_canvas = tk.Canvas(right_frame, bg="#e0e0e0", highlightthickness=0)
    elements_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=elements_canvas.yview)
    elements_scrollable_frame = ttk.Frame(elements_canvas)

    elements_scrollable_frame.bind(
        "<Configure>",
        lambda e: elements_canvas.configure(scrollregion=elements_canvas.bbox("all"))
    )

    elements_canvas.create_window((0, 0), window=elements_scrollable_frame, anchor="nw")
    elements_canvas.configure(yscrollcommand=elements_scrollbar.set)
    elements_canvas.pack(side="left", fill="both", expand=True, padx=(0,5))
    elements_scrollbar.pack(side="right", fill="y")

    # Ajouter les éléments à la liste
    for element in app.elements:
        element_label = DraggableElement(
            elements_scrollable_frame, element, app, is_canvas=False,
            element_data=element, style='Element.TLabel'
        )
        element_label.pack(anchor="w", padx=10, pady=5, fill='x')

    # Configuration de la liste des éléments créés sur la droite
    ttk.Label(right_frame, text="Éléments Créés", font=('Segoe UI', 14, 'bold')).pack(pady=(20, 5))
    created_canvas = tk.Canvas(right_frame, bg="#e0e0e0", highlightthickness=0)
    created_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=created_canvas.yview)
    created_scrollable_frame = ttk.Frame(created_canvas)

    created_scrollable_frame.bind(
        "<Configure>",
        lambda e: created_canvas.configure(scrollregion=created_canvas.bbox("all"))
    )

    created_canvas.create_window((0, 0), window=created_scrollable_frame, anchor="nw")
    created_canvas.configure(yscrollcommand=created_scrollbar.set)
    created_canvas.pack(side="left", fill="both", expand=True, padx=(0,5))
    created_scrollbar.pack(side="right", fill="y")

    # Ajouter les éléments créés à la liste
    for element in app.created_elements:
        element_label = DraggableElement(
            created_scrollable_frame, element, app, is_canvas=False,
            element_data=element, merged=True, style='CreatedElement.TLabel'
        )
        element_label.pack(anchor="w", padx=10, pady=5, fill='x')

    # Assigner created_scrollable_frame à l'application pour un accès facile
    app.created_scrollable_frame = created_scrollable_frame

    # Bouton "Combiner"
    app.combine_button = ttk.Button(
        left_frame, text="Combiner", style='Combine.TButton', command=lambda: app.combine_elements()
    )
    app.combine_button.pack(side="bottom", pady=10, padx=10, anchor="w")

    # Bouton "Supprimer le canvas" (poubelle)
    app.trash_bin = ttk.Button(right_frame, text="🗑️", style='Trash.TButton', command=lambda: app.clear_canvas())
    app.trash_bin.pack(pady=20, ipadx=10, ipady=10)
