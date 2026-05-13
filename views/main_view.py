import tkinter as tk
from tkinter import ttk

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Hồ sơ Bệnh nhân - UHL-FIT")
        self.root.geometry("1100x700")
        self._setup_ui()

    def _setup_ui(self):
        # 1. Toolbar (Import, Export, Giới thiệu, Tìm kiếm)
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side="top", fill="x", padx=10, pady=5)
        
        self.btn_import = ttk.Button(toolbar, text="📁 Import CSV")
        self.btn_import.pack(side="left", padx=2)
        self.btn_export = ttk.Button(toolbar, text="💾 Export CSV")
        self.btn_export.pack(side="left", padx=2)
        self.btn_about = ttk.Button(toolbar, text="ℹ️ Giới thiệu")
        self.btn_about.pack(side="left", padx=2)

        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side="right")
        self.search_col = ttk.Combobox(search_frame, values=["Tất cả", "Họ tên", "Nhóm tuổi"], width=10, state="readonly")
        self.search_col.current(0)
        self.search_col.pack(side="left", padx=2)
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side="left", padx=2)
        self.btn_search = ttk.Button(search_frame, text="🔍 Tìm")
        self.btn_search.pack(side="left", padx=2)
        self.btn_clear = ttk.Button(search_frame, text="❌ Hủy")
        self.btn_clear.pack(side="left", padx=2)

        # 2. Form nhập liệu để Thêm/Sửa
        input_frame = ttk.LabelFrame(self.root, text=" Thông tin chi tiết ", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.entries = {}
        fields = [("Họ tên", "name"), ("Tuổi", "age"), ("Giới tính", "gender"), 
                  ("Cân nặng (kg)", "weight"), ("Chiều cao (cm)", "height"), ("Huyết áp", "bp")]
        for i, (label, key) in enumerate(fields):
            ttk.Label(input_frame, text=f"{label}:").grid(row=i//3, column=(i%3)*2, padx=5, pady=5)
            self.entries[key] = ttk.Entry(input_frame)
            self.entries[key].grid(row=i//3, column=(i%3)*2+1, padx=5, pady=5)

        # 3. Nút chức năng Thêm, Sửa, Xóa
        btn_act = ttk.Frame(self.root)
        btn_act.pack(fill="x", padx=10)
        self.btn_add = ttk.Button(btn_act, text="➕ Thêm")
        self.btn_add.pack(side="left", padx=2)
        self.btn_update = ttk.Button(btn_act, text="📝 Sửa")
        self.btn_update.pack(side="left", padx=2)
        self.btn_delete = ttk.Button(btn_act, text="🗑️ Xóa")
        self.btn_delete.pack(side="left", padx=2)
        
        # Nút thống kê Groupby
        self.btn_stats = ttk.Button(btn_act, text="📊 Thống kê (Groupby)")
        self.btn_stats.pack(side="right", padx=2)

        # 4. Bảng hiển thị (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("id", "n", "a", "g", "b", "gr"), show="headings")
        heads = [("id", "ID", 50), ("n", "Họ tên", 200), ("a", "Tuổi", 80), 
                 ("g", "Giới tính", 100), ("b", "BMI", 100), ("gr", "Nhóm tuổi", 150)]
        for c, h, w in heads:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)