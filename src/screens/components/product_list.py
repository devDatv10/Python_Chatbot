import tkinter as tk
from PIL import Image, ImageTk

def create_product_list(root, products, columns=4):

    # Lalbel for product list
    lbl_products = tk.Label(root, text="Feature products", font=("Arial", 16, "bold"))
    lbl_products.pack(side="top", anchor="w", padx=10)
    frame_products = tk.Frame(root)
    frame_products.pack(pady=10)

    rows = (len(products) + columns - 1) // columns
    
    for i in range(rows):
        row_frame = tk.Frame(frame_products)
        row_frame.pack(fill="x", pady=5)

        for j in range(columns):
            index = i * columns + j
            if index >= len(products):
                break

            product = products[index]
            frame = tk.Frame(row_frame, bd=2, relief="groove")
            frame.pack(side="left", padx=10)

            try:
                img = Image.open(product["image"]).resize((100, 100))
                img = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(frame, image=img)
                lbl_img.image = img
                lbl_img.pack()
            except:
                lbl_img = tk.Label(frame, text="[Không có ảnh]", width=15, height=7, bg="gray")
                lbl_img.pack()

            lbl_name = tk.Label(frame, text=product["name"], font=("Arial", 10))
            lbl_name.pack()

            lbl_buy = tk.Label(frame, text="Mua ngay", font=("Arial", 10, "bold"), fg="blue")
            lbl_buy.pack()

    return frame_products
