import tkinter as tk

def create_header(root, on_entry_focus, on_entry_focusout):
    row1 = tk.Frame(root)
    row1.pack(pady=5, fill="x")

    label_title = tk.Label(row1, text="THẾ GIỚI DI ĐỘNG", font=("Arial", 20, "bold"), fg="black")
    label_title.pack(side="left", padx=10)

    search_entry = tk.Entry(row1, width=40, fg="gray")
    search_entry.insert(0, "Tìm kiếm sản phẩm...")
    search_entry.bind("<FocusIn>", on_entry_focus)
    search_entry.bind("<FocusOut>", on_entry_focusout)
    search_entry.pack(side="left", padx=10, ipady=5)

    btn_login = tk.Button(row1, text="👤 Đăng nhập", font=("Arial", 12))
    btn_login.pack(side="left", padx=5)

    btn_cart = tk.Button(row1, text="🛒 Giỏ hàng", font=("Arial", 12))
    btn_cart.pack(side="left", padx=5)

    return row1, search_entry

