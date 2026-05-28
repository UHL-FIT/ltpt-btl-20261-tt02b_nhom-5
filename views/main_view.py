import tkinter as tk
from tkinter import ttk 

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Hồ sơ Bệnh nhân - UHL-FIT")
        self.root.geometry("1150x780") # Tăng nhẹ chiều cao để hiển thị ghi chú công thức rõ ràng
        self.root.configure(bg="#f5f7fa") 
        
        self.style = ttk.Style()
        self.style.theme_use("clam") 
        self._configure_styles()     
        self._setup_ui()             

    def _configure_styles(self):
        self.style.configure("TFrame", background="#f5f7fa")
        self.style.configure("TLabel", background="#f5f7fa", foreground="#2c3e50", font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="white", bordercolor="#dcdde1")
        self.style.configure("TCombobox", fieldbackground="white", bordercolor="#dcdde1")
        
        self.style.configure("Primary.TButton", background="#008080", foreground="white", font=("Segoe UI", 9, "bold"), borderwidth=0)
        self.style.map("Primary.TButton", background=[("active", "#006666")])
        self.style.configure("Dark.TButton", background="#7f8c8d", foreground="white", font=("Segoe UI", 9, "bold"), borderwidth=0)
        self.style.map("Dark.TButton", background=[("active", "#616a6b")])
        self.style.configure("Success.TButton", background="#2ecc71", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Success.TButton", background=[("active", "#27ae60")])
        self.style.configure("Info.TButton", background="#3498db", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Info.TButton", background=[("active", "#2980b9")])
        self.style.configure("Danger.TButton", background="#e74c3c", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Danger.TButton", background=[("active", "#c0392b")])

        self.style.configure("Treeview", background="#ffffff", foreground="#2c3e50", rowheight=30, font=("Segoe UI", 10))
        self.style.map("Treeview", background=[("selected", "#008080")], foreground=[("selected", "white")])
        self.style.configure("Treeview.Heading", background="#e8ecef", foreground="#2c3e50", font=("Segoe UI", 10, "bold"), padding=6)

    def _setup_ui(self):
        # --- KHU VỰC 1: THANH CÔNG CỤ TRÊN CÙNG ---
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side="top", fill="x", padx=15, pady=10)
        
        self.btn_import = ttk.Button(toolbar, text="📁 Import CSV", style="Primary.TButton")
        self.btn_import.pack(side="left", padx=3)
        self.btn_export = ttk.Button(toolbar, text="💾 Export CSV", style="Primary.TButton")
        self.btn_export.pack(side="left", padx=3)
        self.btn_about = ttk.Button(toolbar, text="ℹ️ Giới thiệu", style="Primary.TButton")
        self.btn_about.pack(side="left", padx=3)

        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side="right")
        
        self.search_col = ttk.Combobox(search_frame, values=["Tất cả", "Họ tên", "Nhóm tuổi", "Giới tính", "Tình trạng SK"], width=12, state="readonly")
        self.search_col.current(0)
        self.search_col.pack(side="left", padx=3)
        
        self.ent_search = ttk.Entry(search_frame, font=("Segoe UI", 10))
        self.ent_search.pack(side="left", padx=3)
        self.btn_search = ttk.Button(search_frame, text="🔍 Tìm", style="Primary.TButton")
        self.btn_search.pack(side="left", padx=3)
        self.btn_clear = ttk.Button(search_frame, text="❌ Hủy", style="Dark.TButton")
        self.btn_clear.pack(side="left", padx=3)

        # --- KHU VỰC 2: HÀNH ĐỘNG THÊM - SỬA - XÓA ---
        btn_act = ttk.Frame(self.root)
        btn_act.pack(fill="x", padx=15, pady=5)
        self.btn_add = ttk.Button(btn_act, text="➕ Thêm bệnh nhân mới", style="Success.TButton")
        self.btn_add.pack(side="left", padx=4)
        self.btn_update = ttk.Button(btn_act, text="📝 Sửa thông tin chọn", style="Info.TButton")
        self.btn_update.pack(side="left", padx=4)
        self.btn_delete = ttk.Button(btn_act, text="🗑️ Xóa bệnh nhân", style="Danger.TButton")
        self.btn_delete.pack(side="left", padx=4)
        
        self.btn_stats = ttk.Button(btn_act, text="📊 Thống kê BMI", style="Primary.TButton", padding=6)
        self.btn_stats.pack(side="right", padx=4)

        # --- KHU VỰC 3: BẢNG TREEVIEW DANH SÁCH ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("id", "n", "a", "g", "b", "gr", "st", "v"), show="headings")
        heads = [
            ("id", "ID", 50), ("n", "Họ tên", 220), ("a", "Tuổi", 60), 
            ("g", "Giới tính", 90), ("b", "BMI", 80), ("gr", "Nhóm tuổi", 130), 
            ("st", "Tình trạng SK (BMI)", 180), ("v", "Số lần khám", 110)
        ]
        for c, h, w in heads:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center")
            
        self.tree.tag_configure("evenrow", background="#f9fbfb") 
        self.tree.tag_configure("oddrow", background="#ffffff")  
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- KHU VỰC 4: KHUNG HỒ SƠ CHI TIẾT ---
        detail_frame = ttk.LabelFrame(self.root, text=" 🔍 HỒ SƠ CHI TIẾT BỆNH NHÂN (Click chọn dòng để xem) ", padding=10)
        detail_frame.pack(fill="x", padx=15, pady=5)
        self.lbl_detail = ttk.Label(detail_frame, text="Chưa chọn bệnh nhân nào từ danh sách bảng.", font=("Segoe UI", 10, "bold"), foreground="#57606f")
        self.lbl_detail.pack(fill="x", padx=5, pady=5)

        # ─── THAY ĐỔI: KHU VỰC 5: KHUNG GHI CHÚ CÔNG THỨC BMI Ở RÌA NGOÀI ───
        formula_frame = ttk.LabelFrame(self.root, text=" 📋 GHI CHÚ Y KHOA: HƯỚNG DẪN THEO DÕI CHỈ SỐ BMI ", padding=10)
        formula_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Nhãn hiển thị công thức toán học tường minh
        lbl_formula_text = ttk.Label(
            formula_frame, 
            text="📐 Công thức tính:  BMI = Cân nặng (kg) / [Chiều cao (m) × Chiều cao (m)]\n"
                 "💡 Mẹo thao tác:  Nhấp đúp chuột (Double-click) vào ô tiêu đề 'ID' để tự động sắp xếp danh sách theo tên bệnh nhân từ A-Z.",
            font=("Segoe UI", 9, "bold"),
            foreground="#008080"
        )
        lbl_formula_text.pack(side="left", fill="x", expand=True)

        # Nhãn hiển thị bảng đối chiếu kết quả chuẩn Châu Á bên cạnh
        lbl_standard_text = ttk.Label(
            formula_frame,
            text="📊 Phân loại thể trạng (Chuẩn Châu Á IDI&WPRO):\n"
                 " • BMI < 18.5: Thiếu cân (Gầy)         • 18.5 ≤ BMI < 23.0: Bình thường\n"
                 " • 23.0 ≤ BMI < 25.0: Thừa cân          • BMI ≥ 25.0: Béo phì",
            font=("Segoe UI", 9, "italic"),
            foreground="#2c3e50",
            justify="left"
        )
        lbl_standard_text.pack(side="right", padx=(20, 10))

    def open_patient_window(self, title, current_data=None):
        """Cửa sổ Popup để thêm/sửa bệnh nhân"""
        win = tk.Toplevel(self.root) 
        win.title(title)
        win.geometry("450x390")
        win.configure(bg="#f5f7fa")
        win.grab_set()  
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=20)
        frame.pack(fill="both", expand=True)

        fields = [
            ("Họ tên", "name"), ("Tuổi", "age"), ("Giới tính", "gender"), 
            ("Cân nặng (kg)", "weight"), ("Chiều cao (cm)", "height"), 
            ("Số lần khám", "visits")
        ]
        
        entries = {}
        for i, (label_text, key) in enumerate(fields):
            lbl_container = ttk.Frame(frame)
            lbl_container.grid(row=i, column=0, padx=(10, 5), pady=8, sticky="e")
            
            lbl_main = ttk.Label(lbl_container, text=f"{label_text}")
            lbl_main.pack(side="left")
            
            if key != "gender":
                lbl_star = tk.Label(lbl_container, text=" *", fg="#e74c3c", bg="#f5f7fa", font=("Segoe UI", 11, "bold"))
                lbl_star.pack(side="left")
                
            lbl_colon = ttk.Label(lbl_container, text=":")
            lbl_colon.pack(side="left")

            if key == "gender":
                entries[key] = ttk.Combobox(frame, values=["Nam", "Nữ", "Khác"], state="readonly", width=22)
                entries[key].current(0)
            else:
                entries[key] = ttk.Entry(frame, width=25, font=("Segoe UI", 10))
            entries[key].grid(row=i, column=1, padx=10, pady=8, sticky="w")

        if current_data:
            entries['name'].insert(0, str(current_data.get('Họ tên', '')))
            entries['age'].insert(0, str(current_data.get('Tuổi', '')))
            entries['gender'].set(str(current_data.get('Giới tính', 'Nam')))
            entries['weight'].insert(0, str(current_data.get('Cân nặng', '')))
            entries['height'].insert(0, str(current_data.get('Chiều cao', '')))
            entries['visits'].insert(0, str(current_data.get('Số lần khám', '1')))

        btn_save = ttk.Button(frame, text="💾 Lưu thông tin", style="Primary.TButton", padding=8)
        btn_save.grid(row=len(fields), column=0, columnspan=2, pady=20)

        return win, entries, btn_save
