import sys
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from components.footer import create_footer
from components.header import create_header
from components.category_menu import create_category_menu
from components.product_list import create_product_list
import pickle
from gensim.models import Word2Vec

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from train import exported_vectorizer, exported_model, exported_topic_map, exported_word2vec_model, exported_answers, predict_answer

model_dir = "./src/models"


def open_chat():
    chat_window.deiconify()

def on_entry_focus(event, entry):
    if entry.get() == "Tìm kiếm sản phẩm...":
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_entry_focusout(event, entry):
    if entry.get().strip() == "":
        entry.insert(0, "Tìm kiếm sản phẩm...")
        entry.config(fg="gray")

def toggle_chat():
    """Hiển thị hoặc ẩn khung chat, và gửi tin nhắn chào từ bot khi mở."""
    global chat_visible
    if chat_visible:
        chat_frame.place_forget()
    else:
        chat_frame.place(x=480, y=150)
        add_message("🤖 Bot: Xin chào! Chúng tôi có thể hỗ trợ gì cho bạn?", "left")
    chat_visible = not chat_visible

def send_message():
    """Gửi tin nhắn của user và phản hồi bot."""
    msg = entry_msg.get().strip()
    if msg:
        add_message(f"Bạn: {msg}", "right")
        entry_msg.delete(0, tk.END) 

        bot_reply = predict_answer(msg, exported_vectorizer, exported_model, exported_topic_map, exported_word2vec_model, exported_answers)
        
        add_message(f"🤖 Bot: {bot_reply}", "left")

def add_message(msg, align="left"):
    """Thêm tin nhắn vào khung chat với căn trái/phải."""
    chat_display.config(state=tk.NORMAL)
    
    if align == "left":
        chat_display.insert(tk.END, f"{msg}\n", "left")
    else:
        chat_display.insert(tk.END, f"{msg}\n", "right")
    
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

def on_entry_focus(event):
    entry = event.widget
    if entry.get() == "Tìm kiếm sản phẩm...":
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_entry_focusout(event):
    entry = event.widget
    if entry.get().strip() == "":
        entry.insert(0, "Tìm kiếm sản phẩm...")
        entry.config(fg="gray")


root = tk.Tk()
root.title("thegioididong.com")
root.geometry("800x600")
chat_visible = False

# Header
header_frame, search_entry = create_header(root, on_entry_focus, on_entry_focusout)

row2 = tk.Frame(root)
row2.pack(pady=5, fill="x")

categories = ["Macbook", "Linux", "Dell", "HP", "Asus", "Lenovo", "Acer", "SamSung", "MSI", "Gaming"]
create_category_menu(root, categories)

# Frame chứa danh sách sản phẩm
frame_products = tk.Frame(root)
frame_products.pack(pady=10)

# Danh sách sản phẩm mẫu
products = [
    {"name": "MacBook Air 2024", "image": "../../images/macbook-air-2024.jpg"},
    {"name": "MacBook Pro 14", "image": "../../images/macbook-pro-14.jpg"},
    {"name": "Macbook Pro 13 inch 2020", "image": "../../images/macbook-pro-13inch-2020.jpg"},
    {"name": "Laptop MacBook Pro 13 2019", "image": "../../images/laptop-macbook-pro-13-2019.jpg"},
    {"name": "Laptop HP 240 G10 i5", "image": "../../images/Laptop-HP-240-G10-i5.jpg"},
    {"name": "Laptop HP HP15-DY2093DX", "image": "../../images/laptop-HP-HP15-DY2093DX.jpg"},
    {"name": "Laptop Dell XPS 13", "image": "../../images/laptopdell-XPS-13.jpg"},
    {"name": "Asus ROG Strix G15", "image": "../../images/asus-rog-strix-G15.jpg"},
]

create_product_list(root, products, columns=4)

# Footer
create_footer(root)

btn_chat = tk.Button(root, text="💬 Chat", font=("Arial", 12), command=toggle_chat, bg="lightblue")
btn_chat.place(x=720, y=520)

chat_frame = tk.Frame(root, width=300, height=350, bg="white", bd=2, relief="ridge")
chat_frame.pack_propagate(False)

chat_display = tk.Text(chat_frame, height=15, width=40, state=tk.DISABLED, bg="white", fg="black")
chat_display.pack(pady=5, padx=5, fill="both", expand=True)

chat_display.tag_configure("left", justify="left", lmargin1=5, lmargin2=5)
chat_display.tag_configure("right", justify="right", rmargin=5)

entry_msg = tk.Entry(chat_frame, width=40, fg="gray")
entry_msg.insert(0, "Nhập tin nhắn...")

entry_msg.bind("<FocusIn>", on_entry_focus)
entry_msg.bind("<FocusOut>", on_entry_focusout)

entry_msg.pack(side="left", fill="x", padx=5, pady=5, expand=True)

btn_send = tk.Button(chat_frame, text="Gửi", command=send_message, bg="green", fg="white")
btn_send.pack(side="right", padx=5, pady=5)

root.mainloop()
