import tkinter as tk

def create_footer(root):
    """Tạo footer với 3 cột: Tổng đài, Công ty, Thông tin khác"""
    footer_frame = tk.Frame(root,  )
    footer_frame.pack(side="bottom", fill="x", pady=10)

    column1 = tk.Frame(footer_frame, )
    column1.pack(side="left", padx=30)

    tk.Label(column1, text="📞 Tổng đài hỗ trợ", font=("Arial", 12, "bold"), ).pack(anchor="w")
    tk.Label(column1, text="Gọi mua hàng: 1800 1060", ).pack(anchor="w")
    tk.Label(column1, text="Khiếu nại: 1800 1062", ).pack(anchor="w")
    tk.Label(column1, text="Bảo hành: 1800 1064", ).pack(anchor="w")

    column2 = tk.Frame(footer_frame, )
    column2.pack(side="left", padx=30)

    tk.Label(column2, text="🏢 Về công ty", font=("Arial", 12, "bold"), ).pack(anchor="w")
    tk.Label(column2, text="Giới thiệu công ty", ).pack(anchor="w")
    tk.Label(column2, text="Tuyển dụng", ).pack(anchor="w")
    tk.Label(column2, text="Chính sách bảo mật", ).pack(anchor="w")

    column3 = tk.Frame(footer_frame, )
    column3.pack(side="left", padx=30)

    tk.Label(column3, text="ℹ️ Thông tin khác", font=("Arial", 12, "bold"), ).pack(anchor="w")
    tk.Label(column3, text="Tích điểm Quà tặng VIP", ).pack(anchor="w")
    tk.Label(column3, text="Lịch sử mua hàng", ).pack(anchor="w")
    tk.Label(column3, text="Chính sách bảo hành", ).pack(anchor="w")

    return footer_frame
