# controllers/bmi_controller.py

from tkinter import Toplevel, messagebox, Tk
from views.login_view import LoginView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime

class BMIController:
    def __init__(self, model, view, user_id):
        self.model = model
        self.view = view
        self.user_id = user_id

    def init_view(self):
        self.view.view_history()

    def calculate_bmi(self):
        try:
            age_str = self.view.get_age()
            height_str = self.view.get_height()
            weight_str = self.view.get_weight()

            if not age_str or not height_str or not weight_str:
                raise ValueError("Vui lòng nhập đầy đủ thông tin.")

            age = int(age_str)
            if age <= 0:
                raise ValueError("Tuổi phải lớn hơn 0.")

            height_cm = float(height_str)
            if height_cm <= 0:
                raise ValueError("Chiều cao phải lớn hơn 0.")
            height = height_cm / 100

            weight = float(weight_str)
            if weight <= 0:
                raise ValueError("Cân nặng phải lớn hơn 0.")

            bmi, category = self.model.calculate_bmi(height, weight)
            self.view.set_result(f"BMI: {bmi:.1f}, {category}")

            self.model.save_bmi(self.user_id, age, height_cm, weight, bmi, category)
            self.view.view_history()

            messagebox.showinfo("Thành công", "Tính BMI và lưu bản ghi thành công!")

            # Clear input fields
            self.view.clear_input_fields()
        except ValueError as e:
            self.view.show_error(str(e))
        except Exception as e:
            self.view.show_error("Đã xảy ra lỗi không mong muốn.")

    def view_history(self):
        history = self.model.get_history(self.user_id)
        self.view.update_history(history)

    def delete_record(self):
        record_id = self.view.get_selected_record_id()
        if record_id is None:
            self.view.show_error("Vui lòng chọn một bản ghi để xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bản ghi này?")
        if confirm:
            self.model.delete_record(record_id)
            self.view.view_history()
            self.view.show_info("Bản ghi đã được xóa.")

    def logout(self):
        from controllers.login_controller import LoginController  # Move import here
        self.view.root.destroy()
        root = Tk()
        login_view = LoginView(root, None)  # Controller will be set after creation
        login_controller = LoginController(self.model, login_view)
        login_view.controller = login_controller
        root.mainloop()

    def view_chart(self):
        history = self.model.get_history(self.user_id)
        if not history:
            self.view.show_error("Không có dữ liệu lịch sử để vẽ biểu đồ.")
            return

        dates = [datetime.strptime(record[7], "%Y-%m-%d %H:%M:%S") for record in history]
        bmis = [record[5] for record in history]

        # Sort the data by date
        dates, bmis = zip(*sorted(zip(dates, bmis)))

        chart_window = Toplevel(self.view.root)
        chart_window.title("Biểu đồ BMI")

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, bmis, marker='o', linestyle='-', color='b', label='BMI')

        ax.set_xlabel('Ngày')
        ax.set_ylabel('BMI')
        ax.set_title('Biểu đồ BMI theo thời gian')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()  # Auto-rotate date labels

        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
