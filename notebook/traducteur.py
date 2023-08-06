# -*- coding: utf-8 -*-
"""
Created on Thu May  4 19:54:36 2023

@author: Narjes
"""

import tkinter as tk
from tkinter import ttk

# Créer la fenêtre principale
root = tk.Tk()
root.title("Traducteur")

# Créer la zone de texte pour l'entrée
entry_label = ttk.Label(root, text="Entrer le texte:")
entry_label.grid(column=0, row=0)
entry_text = tk.Text(root, height=10, width=50)
entry_text.grid(column=0, row=1)

# Créer la zone de texte pour la sortie
output_label = ttk.Label(root, text="Sortie:")
output_label.grid(column=0, row=2)
output_text = tk.Text(root, height=10, width=50)
output_text.grid(column=0, row=3)

# Créer les boutons de traduction et de détection automatique de la langue
translate_button = ttk.Button(root, text="Traduire")
translate_button.grid(column=1, row=1)
detect_button = ttk.Button(root, text="Détection automatique de la langue")
detect_button.grid(column=1, row=2)

# Créer l'assistant vocal
voice_label = ttk.Label(root, text="Assistant vocal:")
voice_label.grid(column=2, row=0)
voice_button = ttk.Button(root, text="Activer l'assistant vocal")
voice_button.grid(column=2, row=1)

# Lancer la boucle principale
root.mainloop()
