import tkinter as tk

def create_category_menu(root, categories):
    row2 = tk.Frame(root)
    row2.pack(pady=5, fill="x")

    for category in categories:
        btn_category = tk.Button(row2, text=category, font=("Arial", 12))
        btn_category.pack(side="left", padx=10)

    return row2
