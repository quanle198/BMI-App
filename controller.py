from model import BMIModel
from view import LoginRegisterView, BMIView
import tkinter as tk

class Controller:
    def __init__(self):
        self.model = BMIModel()
        self.view = None
        self.user_id = None

    def login(self):
        username = self.view.username_entry.get()
        password = self.view.password_entry.get()
        
        self.user_id = self.model.login_user(username, password)
        if self.user_id:
            self.view.root.destroy()
            self.controller = Controller()

            # Tạo cửa sổ chính
            self.root = tk.Tk()

            # Mặc định, hiển thị giao diện đăng nhập và đăng ký
            self.view = BMIView(self.root, self.controller)
        else:
            self.view.show_error("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def register(self):
        username = self.view.username_entry.get()
       
