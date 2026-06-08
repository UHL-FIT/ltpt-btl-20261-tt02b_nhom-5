import tkinter as tk # Thư viện giao diện đồ họa nền tảng của Python
from tkinter import ttk # Thư viện mở rộng (Theme Tkinter) cung cấp các thành phần giao diện phẳng, hiện đại

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Hồ sơ Bệnh nhân - UHL-FIT")
        
        # Thiết lập kích thước cửa sổ mặc định (Rộng x Cao) khi phần mềm vừa khởi chạy
        self.root.geometry("1150x780") 
        
        # Đặt màu nền cho toàn bộ cửa sổ chính (Màu xám trắng dịu mắt, chuẩn y tế)
        self.root.configure(bg="#f5f7fa") 
        
        # Tạo đối tượng Style để tùy biến giao diện cho các thành phần nâng cao (TButton, TCombobox, Treeview...)
        self.style = ttk.Style()
        
        # Ép phần mềm sử dụng gói giao diện "clam" để hệ thống nhận diện việc thay đổi màu nền/màu chữ của các bảng dữ liệu
        self.style.theme_use("clam") 
        
        self._configure_styles()     # Gọi hàm cấu hình màu sắc, phông chữ định sẵn cho hệ thống
        self._setup_ui()             # Gọi hàm sắp xếp và vẽ các nút bấm, bảng danh sách lên màn hình chính

    def _configure_styles(self):
        """Hàm cấu hình thẩm mỹ diện rộng: Đặt màu nền, phông chữ đồng bộ cho toàn ứng dụng"""
        # Cấu hình màu nền cho các khung chứa vật lý (Frame) và các nhãn văn bản chữ thuần (Label)
        self.style.configure("TFrame", background="#f5f7fa")
        self.style.configure("TLabel", background="#f5f7fa", foreground="#2c3e50", font=("Segoe UI", 10))
        
        # Đặt màu trắng cho nền của các ô nhập dữ liệu và hộp chọn Combobox
        self.style.configure("TEntry", fieldbackground="white", bordercolor="#dcdde1")
        self.style.configure("TCombobox", fieldbackground="white", bordercolor="#dcdde1")
        
        # Cấu hình phong cách 'Primary.TButton' (Nút bấm chủ đạo màu xanh Teal, chữ trắng, font đậm)
        self.style.configure("Primary.TButton", background="#008080", foreground="white", font=("Segoe UI", 9, "bold"), borderwidth=0)
        self.style.map("Primary.TButton", background=[("active", "#006666")]) # Tạo hiệu ứng đổi màu sẫm hơn khi di chuột qua nút
        
        # Cấu hình phong cách 'Dark.TButton' (Nút màu xám chì dùng cho chức năng Hủy/Xóa từ khóa)
        self.style.configure("Dark.TButton", background="#7f8c8d", foreground="white", font=("Segoe UI", 9, "bold"), borderwidth=0)
        self.style.map("Dark.TButton", background=[("active", "#616a6b")])
        
        # Cấu hình phong cách 'Success.TButton' (Nút màu xanh lá dùng cho hành động Thêm mới bệnh nhân)
        self.style.configure("Success.TButton", background="#2ecc71", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Success.TButton", background=[("active", "#27ae60")])
        
        # Cấu hình phong cách 'Info.TButton' (Nút màu xanh dương dùng cho hành động Sửa đổi thông tin)
        self.style.configure("Info.TButton", background="#3498db", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Info.TButton", background=[("active", "#2980b9")])
        
        # Cấu hình phong cách 'Danger.TButton' (Nút màu đỏ rực dùng cho hành động Xóa hồ sơ bản ghi)
        self.style.configure("Danger.TButton", background="#e74c3c", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Danger.TButton", background=[("active", "#c0392b")])

        # CẤU HÌNH CHO BẢNG DANH SÁCH (Treeview): Thiết lập màu chữ, chiều cao dòng (30 pixel) và phông chữ
        self.style.configure("Treeview", background="#ffffff", foreground="#2c3e50", rowheight=30, font=("Segoe UI", 10))
        # Khi chọn một dòng, hàng đó sẽ đổi sang màu nền xanh Teal và chữ trắng tinh
        self.style.map("Treeview", background=[("selected", "#008080")], foreground=[("selected", "white")])
        # Cấu hình phần thanh tiêu đề trên cùng của bảng (Chữ đậm, nền xám nhạt)
        self.style.configure("Treeview.Heading", background="#e8ecef", foreground="#2c3e50", font=("Segoe UI", 10, "bold"), padding=6)

    def _setup_ui(self):
        """Hàm dựng bố cục: Sắp xếp các khu vực chức năng trên màn hình chính bằng Layout Manager .pack()"""
        # 1. KHU VỰC THANH CÔNG CỤ TRÊN CÙNG (Toolbar Frame)
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side="top", fill="x", padx=15, pady=10) # fill="x" giúp khung tự động dãn ngang hết màn hình
        
        # Tạo và định vị các nút Import, Export, Giới thiệu ở bên tay trái thanh công cụ
        self.btn_import = ttk.Button(toolbar, text="📁 Import CSV", style="Primary.TButton")
        self.btn_import.pack(side="left", padx=3)
        self.btn_export = ttk.Button(toolbar, text="💾 Export CSV", style="Primary.TButton")
        self.btn_export.pack(side="left", padx=3)
        self.btn_about = ttk.Button(toolbar, text="ℹ️ Giới thiệu", style="Primary.TButton")
        self.btn_about.pack(side="left", padx=3)

        # Tạo một khung phụ bên tay phải của thanh công cụ để chứa khối chức năng Tìm kiếm
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side="right")
        
        # Hộp chọn Combobox giúp người dùng khoanh vùng tìm kiếm (Tất cả, Họ tên, Giới tính...)
        self.search_col = ttk.Combobox(search_frame, values=["Tất cả", "Họ tên", "Nhóm tuổi", "Giới tính", "Tình trạng SK"], width=12, state="readonly")
        self.search_col.current(0) # Đặt mặc định chọn mục đầu tiên là "Tất cả"
        self.search_col.pack(side="left", padx=3)
        
        # Ô gõ từ khóa tìm kiếm (Entry) và các nút bấm lệnh Tìm / Hủy bộ lọc
        self.ent_search = ttk.Entry(search_frame, font=("Segoe UI", 10))
        self.ent_search.pack(side="left", padx=3)
        self.btn_search = ttk.Button(search_frame, text="🔍 Tìm", style="Primary.TButton")
        self.btn_search.pack(side="left", padx=3)
        self.btn_clear = ttk.Button(search_frame, text="❌ Hủy", style="Dark.TButton")
        self.btn_clear.pack(side="left", padx=3)

        # 2. KHU VỰC CÁC NÚT ĐIỀU KHIỂN CHÍNH (Thêm, Sửa, Xóa, Thống kê)
        btn_act = ttk.Frame(self.root)
        btn_act.pack(fill="x", padx=15, pady=5)
        self.btn_add = ttk.Button(btn_act, text="➕ Thêm bệnh nhân mới", style="Success.TButton")
        self.btn_add.pack(side="left", padx=4)
        self.btn_update = ttk.Button(btn_act, text="📝 Sửa thông tin chọn", style="Info.TButton")
        self.btn_update.pack(side="left", padx=4)
        self.btn_delete = ttk.Button(btn_act, text="🗑️ Xóa bệnh nhân", style="Danger.TButton")
        self.btn_delete.pack(side="left", padx=4)
        
        self.btn_stats = ttk.Button(btn_act, text="📊 Thống kê BMI", style="Primary.TButton", padding=6)
        self.btn_stats.pack(side="right", padx=4) # Nút thống kê dạt về góc phải màn hình

        # 3. KHU VỰC BẢNG TRUNG TÂM (Treeview hiển thị danh sách hồ sơ)
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5) # expand=True giúp bảng tự phình to khi phóng to phần mềm

        # Khai báo bảng Treeview gồm 8 cột thông tin chuẩn dữ liệu y tế
        self.tree = ttk.Treeview(table_frame, columns=("id", "n", "a", "g", "b", "gr", "st", "v"), show="headings")
        heads = [
            ("id", "ID", 50), ("n", "Họ tên", 220), ("a", "Tuổi", 60), 
            ("g", "Giới tính", 90), ("b", "BMI", 80), ("gr", "Nhóm tuổi", 130), 
            ("st", "Tình trạng SK (BMI)", 180), ("v", "Số lần khám", 110)
        ]
        for c, h, w in heads:
            self.tree.heading(c, text=h) # Đặt văn bản tiêu đề cột
            self.tree.column(c, width=w, anchor="center") # Định độ rộng và căn dữ liệu ở giữa ô (center)
            
        # Cấu hình màu nền cho thẻ hàng chẵn (evenrow) và hàng lẻ (oddrow) để tạo hiệu ứng đường sọc xen kẽ cực kỳ đẹp mắt
        self.tree.tag_configure("evenrow", background="#f9fbfb") 
        self.tree.tag_configure("oddrow", background="#ffffff")  
        
        # Tích hợp thanh cuộn dọc (Scrollbar) giúp kéo xem danh sách khi số lượng bệnh nhân vượt quá chiều cao màn hình
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 4. KHU VỰC XEM CHI TIẾT HỒ SƠ (Dưới đáy bảng)
        detail_frame = ttk.LabelFrame(self.root, text=" 🔍 HỒ SƠ CHI TIẾT BỆNH NHÂN (Click chọn dòng để xem) ", padding=10)
        detail_frame.pack(fill="x", padx=15, pady=5)
        self.lbl_detail = ttk.Label(detail_frame, text="Chưa chọn bệnh nhân nào từ danh sách bảng.", font=("Segoe UI", 10, "bold"), foreground="#57606f")
        self.lbl_detail.pack(fill="x", padx=5, pady=5)

        # 5. KHU VỰC GHI CHÚ Y KHOA VÀ MẸO ĐIỀU KHIỂN
        formula_frame = ttk.LabelFrame(self.root, text=" 📋 GHI CHÚ Y KHOA: HƯỚNG DẪN THEO DÕI CHỈ SỐ BMI ", padding=10)
        formula_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        lbl_formula_text = ttk.Label(
            formula_frame, 
            text="📐 Công thức tính:  BMI = Cân nặng (kg) / [Chiều cao (m) × Chiều cao (m)]\n"
                 "💡 Mẹo thao tác:  Nhấp đúp chuột (Double-click) vào ô tiêu đề 'ID' để tự động sắp xếp danh sách theo tên bệnh nhân từ A-Z.",
            font=("Segoe UI", 9, "bold"),
            foreground="#008080"
        )
        lbl_formula_text.pack(side="left", fill="x", expand=True)

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
        """Hàm mở Sub Window (Form Popup): Dùng chung cho cả hai nghiệp vụ 'Thêm mới' và 'Sửa đổi' thông tin"""
        win = tk.Toplevel(self.root) # Khởi tạo một cửa sổ con độc lập đè lên trên cửa sổ chính root
        win.title(title)
        win.geometry("450x390")
        win.configure(bg="#f5f7fa")
        
        # ĐÓNG BĂNG CỬA SỔ CHÍNH: Ép người dùng buộc phải tắt hoặc hoàn thành form này mới bấm được ra ngoài
        win.grab_set()  
        win.resizable(False, False) # Chặn không cho kéo dãn thay đổi kích thước form nhập liệu

        frame = ttk.Frame(win, padding=20)
        frame.pack(fill="both", expand=True)

        # Định nghĩa cấu trúc các nhãn và từ khóa tương ứng để sinh ô nhập liệu tự động bằng vòng lặp grid
        fields = [
            ("Họ tên", "name"), ("Tuổi", "age"), ("Giới tính", "gender"), 
            ("Cân nặng (kg)", "weight"), ("Chiều cao (cm)", "height"), 
            ("Số lần khám", "visits")
        ]
        
        entries = {}
        for i, (label_text, key) in enumerate(fields):
            # Tạo một container nhỏ chứa nhãn chữ để căn lề phải cho đẹp mắt
            lbl_container = ttk.Frame(frame)
            lbl_container.grid(row=i, column=0, padx=(10, 5), pady=8, sticky="e")
            
            lbl_main = ttk.Label(lbl_container, text=f"{label_text}")
            lbl_main.pack(side="left")
            
            # Đánh dấu sao màu đỏ (*) biểu thị trường dữ liệu bắt buộc không được để trống (Ngoại trừ ô Giới tính)
            if key != "gender":
                lbl_star = tk.Label(lbl_container, text=" *", fg="#e74c3c", bg="#f5f7fa", font=("Segoe UI", 11, "bold"))
                lbl_star.pack(side="left")
                
            lbl_colon = ttk.Label(lbl_container, text=":")
            lbl_colon.pack(side="left")

            # Phân loại widget: Cột giới tính sử dụng danh sách chọn thả xuống Combobox, các cột khác dùng ô gõ Entry
            if key == "gender":
                entries[key] = ttk.Combobox(frame, values=["Nam", "Nữ", "Khác"], state="readonly", width=22)
                entries[key].current(0)
            else:
                entries[key] = ttk.Entry(frame, width=25, font=("Segoe UI", 10))
            entries[key].grid(row=i, column=1, padx=10, pady=8, sticky="w")

        # NẾU LÀ NGHIỆP VỤ SỬA ĐỔI (Có truyền current_data cũ vào), tự động điền thông tin cũ vào các ô để người dùng chỉnh sửa
        if current_data:
            entries['name'].insert(0, str(current_data.get('Họ tên', '')))
            entries['age'].insert(0, str(current_data.get('Tuổi', '')))
            entries['gender'].set(str(current_data.get('Giới tính', 'Nam')))
            entries['weight'].insert(0, str(current_data.get('Cân nặng', '')))
            entries['height'].insert(0, str(current_data.get('Chiều cao', '')))
            entries['visits'].insert(0, str(current_data.get('Số lần khám', '1')))

        # Tạo nút Lưu thông tin dưới đáy biểu mẫu và trả đối tượng về cho Controller gán sự kiện logic
        btn_save = ttk.Button(frame, text="💾 Lưu thông tin", style="Primary.TButton", padding=8)
        btn_save.grid(row=len(fields), column=0, columnspan=2, pady=20)

        return win, entries, btn_save # Trả về cửa sổ, mảng các ô nhập và nút bấm để Controller tiếp quản
