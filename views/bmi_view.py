# views/bmi_view.py

from tkinter import Tk, Label, Entry, Button, Listbox, messagebox, Toplevel

class BMIView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x300")

        Label(root, text="Tuổi:").grid(row=0, column=0, padx=10, pady=10)
        self.age_entry = Entry(root)
        self.age_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(root, text="Chiều cao (cm):").grid(row=1, column=0, padx=10, pady=10)
        self.height_entry = Entry(root)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(root, text="Cân nặng (kg):").grid(row=2, column=0, padx=10, pady=10)
        self.weight_entry = Entry(root)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=10)

        self.calculate_button = Button(root, text="Tính BMI")
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.history_button = Button(root, text="Xem lịch sử")
        self.history_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.chart_button = Button(root, text="Xem Biểu đồ")
        self.chart_button.grid(row=5, column=0, columnspan=2, pady=10)

        Label(root, text="Kết quả:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.result_label = Label(root, text="")
        self.result_label.grid(row=6, column=1, padx=10, pady=5, sticky='w')

        self.history_listbox = Listbox(root, width=50)
        self.history_listbox.grid(row=7, column=0, columnspan=2, pady=10)

        self.delete_button = Button(root, text="Xóa bản ghi")
        self.delete_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.logout_button = Button(root, text="Đăng xuất")
        self.logout_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Configure grid weights for responsiveness
        for i in range(2):
            root.grid_columnconfigure(i, weight=1)
        for i in range(10):
            root.grid_rowconfigure(i, weight=1)

    def set_controller(self, controller):
        self.controller = controller
        self.calculate_button.config(command=self.controller.calculate_bmi)
        self.history_button.config(command=self.controller.view_history)
        self.chart_button.config(command=self.controller.view_chart)
        self.delete_button.config(command=self.controller.delete_record)
        self.logout_button.config(command=self.controller.logout)

    def get_age(self):
        return self.age_entry.get().strip()

    def get_height(self):
        return self.height_entry.get().strip()

    def get_weight(self):
        return self.weight_entry.get().strip()

    def set_result(self, text):
        self.result_label.config(text=text)

    def update_history(self, records):
        self.history_listbox.delete(0, "end")
        if not records:
            self.history_listbox.insert("end", "Không có dữ liệu lịch sử.")
        else:
            for record in records:
                self.history_listbox.insert("end", f"ID: {record[0]} | Ngày: {record[7]} | BMI: {record[4]:.1f} ({record[5]})")

    def get_selected_record_id(self):
        selected = self.history_listbox.curselection()
        if not selected:
            return None
        record_text = self.history_listbox.get(selected[0])
        try:
            record_id = int(record_text.split(" | ")[0].split(": ")[1])
            return record_id
        except (IndexError, ValueError):
            return None

    def clear_input_fields(self):
        self.age_entry.delete(0, 'end')
        self.height_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')

    def show_error(self, message):
        messagebox.showerror("Lỗi", message)
