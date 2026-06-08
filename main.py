import tkinter as tk
from models.patient_model import PatientModel
from views.main_view import MainView
from controllers.patient_controller import PatientController

if __name__ == "__main__":
    root = tk.Tk()
    model = PatientModel()
    view = MainView(root)
    controller = PatientController(model, view)
    root.mainloop()
