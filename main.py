import tkinter as tk
# Đảm bảo tên Class là PatientModel trùng với nội dung file models/patient_model.py
from models.patient_model import PatientModel
from views.main_view import MainView
from controllers.patient_controller import PatientController

if __name__ == "__main__":
    root = tk.Tk()
    model = PatientModel()
    view = MainView(root)
    controller = PatientController(model, view)
    root.mainloop()