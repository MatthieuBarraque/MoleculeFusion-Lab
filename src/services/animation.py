# src/services/animation.py
import tkinter as tk
from tkinter import ttk
import time

def animate_loading(message, stop_condition):
    """Affiche une animation de chargement avec le message spécifié jusqu'à ce que stop_condition soit vraie."""
    loading_window = tk.Toplevel()
    loading_window.title("Chargement")
    loading_window.geometry("300x100")
    loading_window.grab_set()  # Empêche l'interaction avec la fenêtre principale

    label = ttk.Label(loading_window, text=message)
    label.pack(pady=10)

    progress = ttk.Progressbar(loading_window, mode='indeterminate')
    progress.pack(pady=10, padx=20, fill='x')
    progress.start()

    while not stop_condition():
        loading_window.update_idletasks()
        loading_window.update()
        time.sleep(0.1)

    progress.stop()
    loading_window.destroy()
