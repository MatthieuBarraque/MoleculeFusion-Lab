from tkinter import ttk

def setup_styles():
    """Configure les styles utilisés dans l'application."""
    style = ttk.Style()
    style.theme_use('default')

    # Style pour les éléments
    style.configure('Element.TLabel',
                    background='#FFFFFF',
                    foreground='#000000',
                    padding=5,
                    borderwidth=1,
                    relief='raised')

    # Style pour les éléments créés (fusionnés)
    style.configure('CreatedElement.TLabel',
                    background='#D3D3D3',
                    foreground='#000000',
                    padding=5,
                    borderwidth=1,
                    relief='raised')

    # Style pour l'étiquette de combinaison
    style.configure('Fusion.TLabel',
                    background='#FFD700',
                    foreground='#000000',
                    font=('Segoe UI', 14, 'bold'))

    # Style pour le bouton Combiner
    style.configure('Combine.TButton',
                    foreground='#FFFFFF',
                    background='#4CAF50',
                    font=('Segoe UI', 12, 'bold'))

    # Style pour le bouton Poubelle
    style.configure('Trash.TButton',
                    foreground='#FFFFFF',
                    background='#F44336',
                    font=('Segoe UI', 12, 'bold'))
