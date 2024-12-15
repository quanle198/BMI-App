from tkinter import Tk, Label, Entry, Button, Listbox, messagebox, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LoginRegisterView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Đăng nhập hoặc Đăng ký")

        Label(root, text="Tên đăng nhập:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(root, text="Mật khẩu:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        Button(root, text="Đăng nhập", command=self.controller.login).grid(row=2, column=0, pady=10)
        Button(root, text="Đăng ký", command=self.controller.register).grid(row=2, column=1, pady=10)

class BMIView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("BMI Calculator")

        Label(root, text="Tuổi:").grid(row=0, column=0, padx=10, pady=5)
        self.age_entry = Entry(root)
        self.age_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(root, text="Chiều cao (cm):").grid(row=1, column=0, padx=10, pady=5)
        self.height_entry = Entry(root)
        self.height_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(root, text="Cân nặng (kg):").grid(row=2, column=0, padx=10, pady=5)
        self.weight_entry = Entry(root)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=5)

        Button(root, text="Tính BMI", command=self.controller.calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)
        Button(root, text="Xem lịch sử", command=self.controller.view_history).grid(row=4, column=0, columnspan=2, pady=10)
        Button(root, text="Xem Biểu đồ", command=self.controller.view_chart).grid(row=5, column=0, columnspan=2, pady=10)

        Label(root, text="Kết quả:").grid(row=6, column=0, padx=10, pady=5)
        self.result_label = Label(root, text="")
        self.result_label.grid(row=6, column=1, padx=10, pady=5)

        self.history_listbox = Listbox(root, width=50)
        self.history_listbox.grid(row=7, column=0, columnspan=2, pady=10)

        Button(root, text="Xóa bản ghi", command=self.controller.delete_record).grid(row=8, column=0, columnspan=2, pady=10)
        Button(root, text="Đăng xuất", command=self.controller.logout).grid(row=9, column=0, columnspan=2, pady=10)

    def display_result(self, bmi, category):
        self.result_label.config(text=f"BMI: {bmi:.1f}, {category}")

    def display_history(self, history):
        self.history_listbox.delete(0, "end")
        if not history:
            self.history_listbox.insert("end", "Không có dữ liệu lịch sử.")
        else:
            for record in history:
                self.history_listbox.insert("end", f"ID: {record[0]} | Ngày: {record[7]} | BMI: {record[4]:.1f} ({record[5]})")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)
