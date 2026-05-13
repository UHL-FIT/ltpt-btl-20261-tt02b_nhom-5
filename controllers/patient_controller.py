from tkinter import messagebox, filedialog
import pandas as pd

class PatientController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._bind_events()
        self.refresh()

    def _bind_events(self):
        # Kích hoạt mục Giới thiệu và Thống kê
        self.view.btn_about.config(command=self.show_about)
        self.view.btn_stats.config(command=self.show_stats)
        
        # Thêm, Sửa, Xóa, Tìm kiếm
        self.view.btn_add.config(command=self.add)
        self.view.btn_update.config(command=self.update)
        self.view.btn_delete.config(command=self.delete)
        self.view.btn_search.config(command=self.search)
        self.view.btn_clear.config(command=self.refresh)
        self.view.btn_import.config(command=self.import_csv)
        self.view.btn_export.config(command=self.export_csv)
        self.view.tree.bind("<<TreeviewSelect>>", self.on_select)

    def show_about(self):
        """Kích hoạt mục Giới thiệu"""
        messagebox.showinfo("Giới thiệu", "Nhóm 5 - UHL FIT\nPhần mềm Quản lý Hồ sơ Bệnh nhân\nSử dụng Pandas Groupby & BMI.")

    def show_stats(self):
        """Sử dụng Pandas groupby để tính trung bình theo nhóm tuổi"""
        df = self.model.get_processed_data()
        if df.empty: return
        res = df.groupby('Nhóm tuổi', observed=False)['BMI'].mean().round(2)
        messagebox.showinfo("Thống kê BMI", f"Trung bình BMI theo nhóm tuổi:\n\n{res.to_string()}")

    def refresh(self):
        self.view.ent_search.delete(0, 'end')
        df = self.model.get_processed_data()
        for i in self.view.tree.get_children(): self.view.tree.delete(i)
        for idx, r in df.iterrows():
            self.view.tree.insert("", "end", values=(idx, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], r['Nhóm tuổi']))

    def add(self):
        try:
            data = self.get_inputs()
            self.model.df = pd.concat([self.model.df, pd.DataFrame([data])], ignore_index=True)
            self.model.save()
            self.refresh()
        except: messagebox.showerror("Lỗi", "Kiểm tra dữ liệu nhập!")

    def update(self):
        sel = self.view.tree.selection()
        if not sel: return
        idx = int(self.view.tree.item(sel[0])['values'][0])
        for k, v in self.get_inputs().items(): self.model.df.at[idx, k] = v
        self.model.save()
        self.refresh()

    def delete(self):
        sel = self.view.tree.selection()
        if not sel: return
        idx = int(self.view.tree.item(sel[0])['values'][0])
        self.model.df = self.model.df.drop(idx).reset_index(drop=True)
        self.model.save()
        self.refresh()

    def search(self):
        q = self.view.ent_search.get().lower()
        df = self.model.get_processed_data()
        col = self.view.search_col.get()
        if col == "Họ tên": res = df[df['Họ tên'].str.lower().str.contains(q)]
        elif col == "Nhóm tuổi": res = df[df['Nhóm tuổi'].str.lower().str.contains(q)]
        else: res = df[df.apply(lambda r: r.astype(str).str.lower().str.contains(q).any(), axis=1)]
        
        for i in self.view.tree.get_children(): self.view.tree.delete(i)
        for idx, r in res.iterrows():
            self.view.tree.insert("", "end", values=(idx, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], r['Nhóm tuổi']))

    def get_inputs(self):
        return {
            'Họ tên': self.view.entries['name'].get(),
            'Tuổi': int(self.view.entries['age'].get()),
            'Giới tính': self.view.entries['gender'].get(),
            'Cân nặng': float(self.view.entries['weight'].get()),
            'Chiều cao': float(self.view.entries['height'].get()),
            'Huyết áp': self.view.entries['bp'].get()
        }

    def on_select(self, e):
        sel = self.view.tree.selection()
        if not sel: return
        idx = int(self.view.tree.item(sel[0])['values'][0])
        r = self.model.df.iloc[idx]
        mapping = {'name':'Họ tên', 'age':'Tuổi', 'gender':'Giới tính', 'weight':'Cân nặng', 'height':'Chiều cao', 'bp':'Huyết áp'}
        for k, v in self.view.entries.items():
            v.delete(0, 'end')
            v.insert(0, r[mapping[k]])

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            self.model.df = pd.read_csv(path)
            self.model.save()
            self.refresh()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path: self.model.df.to_csv(path, index=False)