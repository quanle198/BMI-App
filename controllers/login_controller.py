# controllers/login_controller.py

from tkinter import Tk
from views.bmi_view import BMIView
from controllers.bmi_controller import BMIController

class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def login(self):
        username = self.view.get_username()
        password = self.view.get_password()
        if not username or not password:
            self.view.show_error("Vui lòng nhập tên đăng nhập và mật khẩu.")
            return
        user_id = self.model.login_user(username, password)
        if user_id:
            self.view.root.destroy()
            app_root = Tk()
            bmi_view = BMIView(app_root, None)  # Controller will be set after creation
            bmi_controller = BMIController(self.model, bmi_view, user_id)
            bmi_view.set_controller(bmi_controller)
            bmi_controller.init_view()
            app_root.mainloop()
        else:
            self.view.show_error("Tên đăng nhập hoặc mật khẩu không đúng.")

    def register(self):
        username = self.view.get_username()
        password = self.view.get_password()
        if not username or not password:
            self.view.show_error("Vui lòng nhập tên đăng nhập và mật khẩu.")
            return
        success = self.model.register_user(username, password)
        if success:
            self.view.show_info("Đăng ký tài khoản thành công. Hãy đăng nhập.")
            self.view.clear_fields()
        else:
            self.view.show_error("Tên đăng nhập đã tồn tại.")
