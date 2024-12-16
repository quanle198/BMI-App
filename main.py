# main.py

from tkinter import Tk
from views.login_view import LoginView
from controllers.login_controller import LoginController
from models.bmi_model import BMIModel

def run_app():
    root = Tk()
    login_view = LoginView(root, None)  # Controller will be set after creation
    BmiModel = BMIModel()
    login_controller = LoginController(BmiModel, login_view)
    login_view.set_controller(login_controller)
    root.mainloop()

if __name__ == "__main__":
    run_app()
