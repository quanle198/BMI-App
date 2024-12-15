import tkinter as tk
from controller import Controller
from view import LoginRegisterView, BMIView

class App:
    def __init__(self):
        self.controller = Controller()

        # Tạo cửa sổ chính
        self.root = tk.Tk()

        # Mặc định, hiển thị giao diện đăng nhập và đăng ký
        self.view = LoginRegisterView(self.root, self.controller)
        self.controller.view = self.view

        self.root.mainloop()

if __name__ == "__main__":
    app = App()
