from tkinter import messagebox, filedialog
import pandas as pd
from utils.logger import setup_logger

class PatientController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.logger = setup_logger("patient_controller")
        self._bind_events() 
        self.refresh()      

    def _bind_events(self):
        self.view.btn_about.config(command=self.show_about)
        self.view.btn_stats.config(command=self.show_stats)
        self.view.btn_add.config(command=self.open_add_dialog)
        self.view.btn_update.config(command=self.open_edit_dialog)
        self.view.btn_delete.config(command=self.delete)
        self.view.btn_search.config(command=self.search)
        self.view.btn_clear.config(command=self.refresh)
        self.view.btn_import.config(command=self.import_csv)
        self.view.btn_export.config(command=self.export_csv)
        self.view.tree.bind("<<TreeviewSelect>>", self.show_detail_panel)
        self.view.tree.bind("<Double-1>", self.handle_double_click)

    def handle_double_click(self, event):
        region = self.view.tree.identify_region(event.x, event.y)
        column = self.view.tree.identify_column(event.x)
        if region in ("heading", "cell") and column == "#1":
            self.model.sort_by_name()
            self.model.save()
            self.refresh()

    def show_about(self):
        messagebox.showinfo("Giới thiệu", "Nhóm 5 - UHL FIT\nPhần mềm Quản lý Hồ sơ Bệnh nhân.")

    def show_stats(self):
        df = self.model.get_processed_data()
        if df.empty: return
        res = df.groupby('Nhóm tuổi', observed=False)['BMI'].mean().round(2)
        messagebox.showinfo("Thống kê BMI", f"Trung bình BMI theo nhóm tuổi:\n\n{res.to_string()}")

    def refresh(self):
        self.view.ent_search.delete(0, 'end')
        df = self.model.get_processed_data()  
        self.view.lbl_detail.config(text="Chưa chọn bệnh nhân nào từ danh sách bảng.", foreground="#57606f")
        for i in self.view.tree.get_children(): self.view.tree.delete(i) 
        for count, (idx, r) in enumerate(df.iterrows()):
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            self.view.tree.insert("", "end", values=(
                idx + 1, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], 
                r['Nhóm tuổi'], r['Trạng thái hiển thị'], r['Số lần khám']
            ), tags=(row_tag,))

    # ─── THÊM MỚI: Hàm kiểm tra chuỗi nhập vào có phải số dương lớn hơn 0 không ───
    def _validate_positive_number(self, value, field_name):
        """Trả về giá trị float nếu hợp lệ, trả về None nếu không phải số dương > 0"""
        try:
            num = float(value)
            if num <= 0:
                messagebox.showwarning("Dữ liệu sai quy định", f"Trường '{field_name}' bắt buộc phải là số lớn hơn 0!")
                return None
            return num
        except ValueError:
            messagebox.showerror("Lỗi định dạng", f"Trường '{field_name}' phải nhập vào định dạng số hợp lệ!")
            return None

    def open_add_dialog(self):
        win, entries, btn_save = self.view.open_patient_window("Thêm bệnh nhân mới")
        def save_action():
            name = entries['name'].get().strip()
            if not name:
                messagebox.showwarning("Cảnh báo dữ liệu", "Họ tên bệnh nhân không được để trống!")
                return
            
            # Kiểm tra nghiêm ngặt điều kiện số dương > 0 cho từng trường
            age_val = self._validate_positive_number(entries['age'].get(), "Tuổi")
            if age_val is None: return
            
            weight_val = self._validate_positive_number(entries['weight'].get(), "Cân nặng")
            if weight_val is None: return
            
            height_val = self._validate_positive_number(entries['height'].get(), "Chiều cao")
            if height_val is None: return
            
            visits_val = self._validate_positive_number(entries['visits'].get(), "Số lần khám")
            if visits_val is None: return

            # Nếu tất cả đều vượt qua bài kiểm tra thì tiến hành lưu dữ liệu
            data = {
                'Họ tên': name, 'Tuổi': str(int(age_val)), 'Giới tính': entries['gender'].get(),
                'Cân nặng': str(weight_val), 'Chiều cao': str(height_val), 'Số lần khám': str(int(visits_val))
            }
            self.model.df = pd.concat([self.model.df, pd.DataFrame([data])], ignore_index=True)
            self.model.save()      
            self.refresh()         
            win.destroy()          
            messagebox.showinfo("Thành công", "Đã thêm bệnh nhân thành công!")
            
        btn_save.config(command=save_action)

    def open_edit_dialog(self):
        sel = self.view.tree.selection() 
        if not sel: 
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng bệnh nhân để sửa!")
            return
        display_id = int(self.view.tree.item(sel[0])['values'][0])
        idx = display_id - 1
        current_data = self.model.df.iloc[idx].to_dict() 
        win, entries, btn_save = self.view.open_patient_window("Chỉnh sửa thông tin bệnh nhân", current_data)
        
        def save_action():
            name = entries['name'].get().strip()
            if not name: return
            
            # Kiểm tra nghiêm ngặt điều kiện số dương > 0 cho từng trường khi sửa
            age_val = self._validate_positive_number(entries['age'].get(), "Tuổi")
            if age_val is None: return
            
            weight_val = self._validate_positive_number(entries['weight'].get(), "Cân nặng")
            if weight_val is None: return
            
            height_val = self._validate_positive_number(entries['height'].get(), "Chiều cao")
            if height_val is None: return
            
            visits_val = self._validate_positive_number(entries['visits'].get(), "Số lần khám")
            if visits_val is None: return

            # Cập nhật vào RAM sau khi kiểm tra thành công
            self.model.df.at[idx, 'Họ tên'] = name
            self.model.df.at[idx, 'Tuổi'] = str(int(age_val))
            self.model.df.at[idx, 'Giới tính'] = entries['gender'].get()
            self.model.df.at[idx, 'Cân nặng'] = str(weight_val)
            self.model.df.at[idx, 'Chiều cao'] = str(height_val)
            self.model.df.at[idx, 'Số lần khám'] = str(int(visits_val))
            
            self.model.save() 
            self.refresh()    
            win.destroy()     
            messagebox.showinfo("Thành công", "Đã cập nhật thay đổi thành công!")
            
        btn_save.config(command=save_action)

    def show_detail_panel(self, event):
        sel = self.view.tree.selection()
        if not sel or len(sel) > 1: return
        display_id = int(self.view.tree.item(sel[0])['values'][0])
        idx = display_id - 1
        raw_data = self.model.df.iloc[idx]
        processed_df = self.model.get_processed_data().iloc[idx]
        detail_text = (
            f"👤 Họ và tên: {str(raw_data['Họ tên']).upper()}  |  "
            f"🎂 Tuổi: {raw_data['Tuổi']} ({processed_df['Nhóm tuổi']})  |  "
            f"⚥ Giới tính: {raw_data['Giới tính']}\n"
            f"⚖️ Cân nặng: {raw_data['Cân nặng']} kg  |  "
            f"📏 Chiều cao: {raw_data['Chiều cao']} cm  |  "
            f"📈 Chỉ số BMI: {processed_df['BMI']}  |  "
            f"🩺 Tình trạng sức khỏe: {processed_df['Trạng thái hiển thị']}  |  "
            f"🏥 Số lần khám: {processed_df['Số lần khám']} lần"
        )
        self.view.lbl_detail.config(text=detail_text, foreground="#1e272e")

    def delete(self):
        sel = self.view.tree.selection()
        if not sel: return
        display_id = int(self.view.tree.item(sel[0])['values'][0])
        idx = display_id - 1
        patient_name = self.model.df.iloc[idx]['Họ tên']
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa bệnh nhân '{patient_name}' không?"):
            self.model.df = self.model.df.drop(idx).reset_index(drop=True)
            self.model.save()
            self.refresh()

    def search(self):
        q = self.view.ent_search.get().lower().strip() 
        col = self.view.search_col.get() 
        df = self.model.get_processed_data()
        if col == "Họ tên": res = df[df['Họ tên'].str.lower().str.contains(q, na=False)]
        elif col == "Nhóm tuổi": res = df[df['Nhóm tuổi'].str.lower().str.contains(q, na=False)]
        elif col == "Giới tính": res = df[df['Giới tính'].str.lower().str.contains(q, na=False)]
        elif col == "Tình trạng SK": res = df[df['Trạng thái hiển thị'].str.lower().str.contains(q, na=False)]
        else: res = df[df.apply(lambda r: r.astype(str).str.lower().str.contains(q).any(), axis=1)]
        
        for i in self.view.tree.get_children(): self.view.tree.delete(i)
        for count, (idx, r) in enumerate(res.iterrows()):
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            self.view.tree.insert("", "end", values=(
                idx + 1, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], 
                r['Nhóm tuổi'], r['Trạng thái hiển thị'], r['Số lần khám']
            ), tags=(row_tag,))

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            try:
                self.model.df = pd.read_csv(path, dtype=str)
                if 'Huyết áp' in self.model.df.columns: self.model.df = self.model.df.drop(columns=['Huyết áp'])
                if 'Số lần khám' not in self.model.df.columns: self.model.df['Số lần khám'] = "1"
                self.model.save(); self.refresh()
            except Exception: messagebox.showerror("Lỗi tệp", "Cấu trúc tệp CSV ngoài không tương thích!")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path: self.model.df.to_csv(path, index=False)
