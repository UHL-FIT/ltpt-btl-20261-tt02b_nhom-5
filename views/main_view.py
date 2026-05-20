import tkinter as tk
from tkinter import ttk  # Thư viện giao diện mở rộng (Themed Tkinter) cung cấp các linh kiện giao diện đẹp hơn

class MainView:
    def __init__(self, root):
        """
        Hàm khởi tạo màn hình giao diện chính.
        Giải thích tham số 'root': Cửa sổ tổng chính (Tk) được truyền từ file khởi chạy main.py vào.
        """
        self.root = root
        self.root.title("Quản lý Hồ sơ Bệnh nhân - UHL-FIT")
        self.root.geometry("1150x740") # Quy định kích thước màn hình mặc định rộng x cao
        self.root.configure(bg="#f5f7fa") # Đổi màu nền background tổng thể sang màu xám trắng dịu mắt
        
        self.style = ttk.Style()
        self.style.theme_use("clam") # Sử dụng theme 'clam' để có toàn quyền ghi đè phối màu cho linh kiện
        self._configure_styles()     # Gọi hàm cấu hình bảng màu CSS
        self._setup_ui()             # Gọi hàm xây dựng bố cục các nút bấm và bảng dữ liệu

    def _configure_styles(self):
        """
        HÀM PHỐI MÀU GIAO DIỆN (Đạt chuẩn thẩm mỹ bài tập lớn, loại bỏ giao diện xám xịt mặc định):
        Đóng vai trò thiết lập màu nền, màu chữ, bo góc mờ tương tự như viết CSS.
        """
        self.style.configure("TFrame", background="#f5f7fa")
        self.style.configure("TLabel", background="#f5f7fa", foreground="#2c3e50", font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="white", bordercolor="#dcdde1")
        self.style.configure("TCombobox", fieldbackground="white", bordercolor="#dcdde1")
        
        # Thiết kế nút bấm Màu Xanh Teal chủ đạo (Cho các tính năng chung, tra cứu, hệ thống)
        self.style.configure("Primary.TButton", background="#008080", foreground="white", font=("Segoe UI", 9, "bold"), borderwidth=0)
        self.style.map("Primary.TButton", background=[("active", "#006666")]) # Hiệu ứng đổi màu tối hơn khi di chuột vào
        
        # Thiết kế nút bấm Màu Xám Đậm (Dành cho chức năng Hủy bỏ hành động)
        self.style.configure("Dark.TButton", background="#7f8c8d", foreground="white", font=("Segoe UI", 9, "bold"), borderwidth=0)
        self.style.map("Dark.TButton", background=[("active", "#616a6b")])

        # Thiết kế nút bấm Màu Xanh Lá Cây - Tượng trưng cho hành động THÊM MỚI dữ liệu an toàn
        self.style.configure("Success.TButton", background="#2ecc71", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Success.TButton", background=[("active", "#27ae60")])
        
        # Thiết kế nút bấm Màu Xanh Dương - Tượng trưng cho hành động SỬA ĐỔI, cập nhật thông tin
        self.style.configure("Info.TButton", background="#3498db", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Info.TButton", background=[("active", "#2980b9")])
        
        # Thiết kế nút bấm Màu Đỏ - Tượng trưng cho hành động XÓA dữ liệu nguy hiểm cần chú ý
        self.style.configure("Danger.TButton", background="#e74c3c", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Danger.TButton", background=[("active", "#c0392b")])

        # Thiết lập kiểu dáng cho Bảng Treeview (Màu chữ xanh đen, chiều cao dòng 30px thông thoáng)
        self.style.configure("Treeview", background="#ffffff", foreground="#2c3e50", rowheight=30, font=("Segoe UI", 10))
        # Khi dòng được click chọn, bôi nền xanh Teal và chữ chuyển sang màu Trắng nổi bật
        self.style.map("Treeview", background=[("selected", "#008080")], foreground=[("selected", "white")])
        # Kiểu dáng tiêu đề cột của bảng (Chữ in đậm, nền xám nhạt tinh tế)
        self.style.configure("Treeview.Heading", background="#e8ecef", foreground="#2c3e50", font=("Segoe UI", 10, "bold"), padding=6)

    def _setup_ui(self):
        """Hàm dựng khung và sắp xếp vị trí các linh kiện lên màn hình chính theo trục dọc (pack)"""
        
        # ==========================================
        # --- KHU VỰC 1: THANH CÔNG CỤ TRÊN CÙNG (Toolbar Frame) ---
        # ==========================================
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side="top", fill="x", padx=15, pady=10)
        
        # Các nút bấm chức năng hệ thống, sắp xếp dồn sang phía bên trái (side="left")
        self.btn_import = ttk.Button(toolbar, text="📁 Import CSV", style="Primary.TButton")
        self.btn_import.pack(side="left", padx=3)
        self.btn_export = ttk.Button(toolbar, text="💾 Export CSV", style="Primary.TButton")
        self.btn_export.pack(side="left", padx=3)
        self.btn_about = ttk.Button(toolbar, text="ℹ️ Giới thiệu", style="Primary.TButton")
        self.btn_about.pack(side="left", padx=3)

        # Khung chứa bộ lọc tìm kiếm nâng cao, sắp xếp dồn sang góc bên phải (side="right")
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side="right")
        
        # Thanh menu chọn cột cần tìm kiếm (Combobox), state="readonly" để khóa không cho người dùng tự gõ chữ phá cấu trúc
        self.search_col = ttk.Combobox(search_frame, values=["Tất cả", "Họ tên", "Nhóm tuổi", "Giới tính", "Tình trạng SK"], width=12, state="readonly")
        self.search_col.current(0) # Mặc định chọn vị trí số 0 là lọc 'Tất cả'
        self.search_col.pack(side="left", padx=3)
        
        self.ent_search = ttk.Entry(search_frame, font=("Segoe UI", 10))
        self.ent_search.pack(side="left", padx=3)
        self.btn_search = ttk.Button(search_frame, text="🔍 Tìm", style="Primary.TButton")
        self.btn_search.pack(side="left", padx=3)
        self.btn_clear = ttk.Button(search_frame, text="❌ Hủy", style="Dark.TButton")
        self.btn_clear.pack(side="left", padx=3)

        # ==========================================
        # --- KHU VỰC 2: THANH NÚT HÀNH ĐỘNG CHÍNH (Thêm/Sửa/Xóa/Thống kê) ---
        # ==========================================
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

        # ==========================================
        # --- KHU VỰC 3: BẢNG TREEVIEW HIỂN THỊ DANH SÁCH ---
        # ==========================================
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Khởi tạo bảng Treeview với 8 cột tương ứng dữ liệu cần xuất ra màn hình chính
        self.tree = ttk.Treeview(table_frame, columns=("id", "n", "a", "g", "b", "gr", "st", "v"), show="headings")
        
        # Cấu trúc mảng cấu hình tiêu đề (Mã cột, Tên hiển thị, Chiều rộng cột bằng đơn vị pixel)
        heads = [
            ("id", "ID", 50), ("n", "Họ tên", 220), ("a", "Tuổi", 60), 
            ("g", "Giới tính", 90), ("b", "BMI", 80), ("gr", "Nhóm tuổi", 130), 
            ("st", "Tình trạng SK", 160), ("v", "Số lần khám", 110)
        ]
        for c, h, w in heads:
            self.tree.heading(c, text=h) # Đặt tên hiển thị cho đầu cột
            self.tree.column(c, width=w, anchor="center") # Căn chữ nằm ở chính giữa ô (center)
            
        # Định nghĩa màu sắc sọc bảng xen kẽ để giao diện trực quan, dễ theo dõi dòng
        self.tree.tag_configure("evenrow", background="#f9fbfb") # Dòng chẵn màu trắng xanh ngọc mờ
        self.tree.tag_configure("oddrow", background="#ffffff")  # Dòng lẻ màu trắng tinh khiết
        
        # Khởi tạo thanh cuộn chuột dọc (Scrollbar) phòng trường hợp danh sách bệnh nhân quá dài vượt màn hình
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set) # Liên kết thanh cuộn chặt chẽ với Treeview
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ==========================================
        # --- KHU VỰC 4: KHUNG HỒ SƠ CHI TIẾT (Detail Panel) ---
        # ==========================================
        # LabelFrame tạo ra một chiếc hộp bo viền bao quanh kèm tiêu đề chữ rất lịch sự
        detail_frame = ttk.LabelFrame(self.root, text=" 🔍 HỒ SƠ CHI TIẾT BỆNH NHÂN (Click chọn dòng để xem) ", padding=10)
        detail_frame.pack(fill="x", padx=15, pady=5)
        
        # Nhãn chữ hiển thị thông tin toàn bộ hồ sơ của người được chọn, mặc định ban đầu thông báo chưa chọn ai
        self.lbl_detail = ttk.Label(
            detail_frame, 
            text="Chưa chọn bệnh nhân nào từ danh sách bảng.",
            font=("Segoe UI", 10, "bold"),
            foreground="#57606f",
            justify="left"
        )
        self.lbl_detail.pack(fill="x", padx=5, pady=5)

        # ==========================================
        # --- KHU VỰC 5: KHU VỰC TRÌNH BÀY CÔNG THỨC BMI Ở CUỐI BẢNG ---
        # ==========================================
        formula_frame = ttk.Frame(self.root)
        formula_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        lbl_formula = ttk.Label(
            formula_frame, 
            text="💡 Hướng dẫn y khoa: Chỉ số BMI = Cân nặng (kg) / [Chiều cao (m) × Chiều cao (m)]. "
                 "Hệ thống sẽ tự động quy đổi từ đơn vị cm nhập vào form sang mét trước khi tính toán.",
            font=("Segoe UI", 9, "italic"),
            foreground="#57606f",
            anchor="w"
        )
        lbl_formula.pack(side="left", fill="x")

    def open_patient_window(self, title, current_data=None):
        """
        HÀM POPUP ĐA NĂNG (Dùng chung cho cả hành động THÊM mới và SỬA thông tin):
        Tự động mở ra một cửa sổ nhỏ độc lập nằm đè lên màn hình chính khi click nút Thêm/Sửa.
        """
        win = tk.Toplevel(self.root) # Khởi tạo cửa sổ con cấp cao Toplevel
        win.title(title)
        win.geometry("420x420")
        win.configure(bg="#f5f7fa")
        win.grab_set()  # CHẶN và KHÓA hoàn toàn màn hình chính ở phía sau (Bắt buộc phải xử lý xong popup này mới quay lại được app)
        win.resizable(False, False) # Khóa không cho kéo giãn kích thước cửa sổ nhập liệu

        frame = ttk.Frame(win, padding=20)
        frame.pack(fill="both", expand=True)

        # Danh sách các trường nhập liệu (Tên hiển thị form giao diện, Mã key để lưu từ điển)
        fields = [
            ("Họ tên", "name"), ("Tuổi", "age"), ("Giới tính", "gender"), 
            ("Cân nặng (kg)", "weight"), ("Chiều cao (cm)", "height"), 
            ("Huyết áp (Thu/Trương)", "bp"), ("Số lần khám", "visits")
        ]
        
        entries = {} # Từ điển trống dùng để quản lý lưu trữ các đối tượng Entry biến nhập liệu
        for i, (label, key) in enumerate(fields):
            # Tạo chữ nhãn mô tả ở cột 0, căn lề phải (sticky="e")
            ttk.Label(frame, text=f"{label}:").grid(row=i, column=0, padx=10, pady=8, sticky="e")
            
            if key == "gender":
                # Riêng trường Giới tính, tạo thanh Combobox cho chọn sẵn, tránh người dùng gõ lung tung chữ
                entries[key] = ttk.Combobox(frame, values=["Nam", "Nữ", "Khác"], state="readonly", width=22)
                entries[key].current(0)
            else:
                # Các trường còn lại tạo ô nhập văn bản Entry thông thường ở cột 1
                entries[key] = ttk.Entry(frame, width=25, font=("Segoe UI", 10))
                
            entries[key].grid(row=i, column=1, padx=10, pady=8, sticky="w")

        # LOGIC NẠP ĐÈ DỮ LIỆU CŨ (Chỉ chạy khi người dùng ấn nút SỬA):
        # Nếu có dữ liệu cũ truyền vào (current_data không trống), tiến hành nhồi chữ cũ vào các ô form nhập liệu
        if current_data:
            entries['name'].insert(0, str(current_data.get('Họ tên', '')))
            entries['age'].insert(0, str(current_data.get('Tuổi', '')))
            entries['gender'].set(str(current_data.get('Giới tính', 'Nam')))
            entries['weight'].insert(0, str(current_data.get('Cân nặng', '')))
            entries['height'].insert(0, str(current_data.get('Chiều cao', '')))
            entries['bp'].insert(0, str(current_data.get('Huyết áp', '')))
            entries['visits'].insert(0, str(current_data.get('Số lần khám', '1')))

        # Tạo nút Lưu thông tin ở hàng cuối cùng của Grid layout
        btn_save = ttk.Button(frame, text="💾 Lưu thông tin", style="Primary.TButton", padding=8)
        btn_save.grid(row=len(fields), column=0, columnspan=2, pady=20)

        # Trả các thực thể điều khiển về cho hàm save_action ở Controller toàn quyền xử lý sự kiện lưu tệp
        return win, entries, btn_save
