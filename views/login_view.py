# views/login_view.py

from tkinter import Tk, Label, Entry, Button, messagebox

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Đăng nhập")
        self.root.geometry("300x150")

        Label(root, text="Tên đăng nhập:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(root, text="Mật khẩu:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = Button(root, text="Đăng nhập")
        self.login_button.grid(row=2, column=0, pady=10)

        self.register_button = Button(root, text="Đăng ký")
        self.register_button.grid(row=2, column=1, pady=10)

    def set_controller(self, controller):
        self.controller = controller
        self.login_button.config(command=self.controller.login)
        self.register_button.config(command=self.controller.register)

    def get_username(self):
        return self.username_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def show_error(self, message):
        messagebox.showerror("Lỗi", message)

    def show_info(self, message):
        messagebox.showinfo("Thông báo", message)

    def clear_fields(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
