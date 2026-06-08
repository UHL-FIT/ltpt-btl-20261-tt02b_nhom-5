from tkinter import messagebox, filedialog # Nạp công cụ làm hộp thoại thông báo và hộp thoại chọn file của hệ điều hành
import pandas as pd # Nạp thư viện Pandas để hỗ trợ xử lý mảng và nối bảng dữ liệu
from utils.logger import setup_logger # Nạp hệ thống ghi log hoạt động

class PatientController:
    def __init__(self, model, view):
        self.model = model # Liên kết tầng Controller với tầng dữ liệu Model
        self.view = view   # Liên kết tầng Controller với tầng giao diện đồ họa View
        self.logger = setup_logger("patient_controller") # Khởi tạo logger riêng cho lớp điều phối
        self._bind_events() # Kích hoạt hàm liên kết lắng nghe toàn bộ sự kiện click chuột trên màn hình
        self.refresh()      # Tiến hành quét và nạp dữ liệu lên bảng danh sách ngay khi vừa mở phần mềm

    def _bind_events(self):
        """Hàm liên kết (Binding): Cài đặt hành động cho từng nút bấm trên giao diện View"""
        self.view.btn_about.config(command=self.show_about)   # Bấm nút Giới thiệu -> Chạy hàm show_about
        self.view.btn_stats.config(command=self.show_stats)   # Bấm nút Thống kê -> Chạy hàm show_stats
        self.view.btn_add.config(command=self.open_add_dialog) # Bấm nút Thêm -> Mở form cửa sổ popup thêm mới
        self.view.btn_update.config(command=self.open_edit_dialog) # Bấm nút Sửa -> Mở form sửa thông tin chọn
        self.view.btn_delete.config(command=self.delete)       # Bấm nút Xóa -> Kích hoạt quy trình xóa bản ghi
        self.view.btn_search.config(command=self.search)       # Bấm nút Tìm -> Thực hiện lọc danh sách
        self.view.btn_clear.config(command=self.refresh)       # Bấm nút Hủy -> Xóa từ khóa tìm kiếm, tải lại bảng đầy đủ
        self.view.btn_import.config(command=self.import_csv)   # Bấm nút Import CSV -> Gọi hộp thoại chọn file nạp vào
        self.view.btn_export.config(command=self.export_csv)   # Bấm nút Export CSV -> Gọi hộp thoại lưu file ra ngoài
        
        # Lắng nghe sự kiện click chuột chọn dòng trên bảng danh sách Treeview -> Hiện thông tin xuống khung chi tiết
        self.view.tree.bind("<<TreeviewSelect>>", self.show_detail_panel)
        
        # Lắng nghe sự kiện người dùng nhấp đúp chuột trái (<Double-1>) vào tiêu đề bảng để kích hoạt sắp xếp
        self.view.tree.bind("<Double-1>", self.handle_double_click)

    def handle_double_click(self, event):
        """Hàm xử lý sự kiện nhấp đúp chuột trái vào tiêu đề cột ID để sắp xếp tên bệnh nhân"""
        region = self.view.tree.identify_region(event.x, event.y) # Xác định vị trí click chuột thuộc vùng nào
        column = self.view.tree.identify_column(event.x)          # SỬA LỖI HÌNH 1: Chỉ truyền event.x để lấy đúng mã cột
        
        # Nếu vị trí click nằm ở phần tiêu đề đầu trang (heading) hoặc ô dữ liệu và thuộc cột đầu tiên (#1 tức cột ID)
        if region in ("heading", "cell") and column == "#1":
            self.model.sort_by_name() # Ra lệnh cho Model thực hiện đảo thứ tự sắp xếp mảng dữ liệu
            self.model.save()         # Lưu lại thứ tự mới sắp xếp vào cơ sở dữ liệu CSV
            self.refresh()            # Làm mới lại bảng hiển thị giao diện để cập nhật thứ tự mới cho người dùng

    def show_about(self):
        """Hiển thị hộp thoại popup thông tin bản quyền phần mềm"""
        messagebox.showinfo("Giới thiệu", "Nhóm 5 - UHL FIT\nPhần mềm Quản lý Hồ sơ Bệnh nhân.")

    def show_stats(self):
        """Hàm thống kê nâng cao: Tính toán và hiển thị điểm trung bình BMI phân tách theo từng nhóm tuổi"""
        df = self.model.get_processed_data() # Lấy bảng dữ liệu tạm đã được tính sẵn chỉ số BMI động
        if df.empty: return # Nếu hệ thống không có dữ liệu thì thoát hàm
        
        # Áp dụng thuật toán gom nhóm groupby của Pandas theo cột 'Nhóm tuổi' và tính giá trị trung bình (.mean) của cột BMI
        res = df.groupby('Nhóm tuổi', observed=False)['BMI'].mean().round(2)
        
        # Đổ kết quả toán học ra màn hình bằng một hộp thoại trực quan chữ văn bản (to_string)
        messagebox.showinfo("Thống kê BMI", f"Trung bình BMI theo nhóm tuổi:\n\n{res.to_string()}")

    def refresh(self):
        """Hàm làm mới toàn diện: Xóa sạch dữ liệu cũ trên bảng giao diện và nạp đồng bộ dữ liệu mới tinh từ file CSV"""
        self.view.ent_search.delete(0, 'end') # Dọn sạch văn bản trong ô nhập tìm kiếm
        df = self.model.get_processed_data()  # Đọc bảng dữ liệu chuẩn đã xử lý y khoa từ Model lên
        
        # Đặt lại trạng thái mặc định cho khung hiển thị hồ sơ chi tiết nằm ở phía dưới cùng
        self.view.lbl_detail.config(text="Chưa chọn bệnh nhân nào từ danh sách bảng.", foreground="#57606f")
        
        # Vòng lặp dọn rác: Xóa sạch toàn bộ các dòng đang hiển thị trên bảng Treeview giao diện để chuẩn bị nạp dòng mới
        for i in self.view.tree.get_children(): 
            self.view.tree.delete(i) 
            
        # Duyệt qua từng dòng dữ liệu trong bảng DataFrame bằng hàm iterrows() của thư viện Pandas
        for count, (idx, r) in enumerate(df.iterrows()):
            # Thuật toán thẩm mỹ: Dòng thứ tự chẵn dùng thẻ màu 'evenrow', dòng lẻ dùng thẻ màu 'oddrow' (tạo hiệu ứng sọc kẻ)
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            
            # Nạp một dòng dữ liệu hoàn chỉnh vào widget Treeview của tầng View để người dùng nhìn thấy
            self.view.tree.insert("", "end", values=(
                idx + 1, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], 
                r['Nhóm tuổi'], r['Trạng thái hiển thị'], r['Số lần khám']
            ), tags=(row_tag,))

    def _validate_positive_number(self, value, field_name):
        """HÀM KIỂM TRA ĐIỀU KIỆN (VALIDATION): Chặn hoàn toàn số âm, số bằng 0 và chữ viết sai ô"""
        try:
            num = float(value) # Thử nghiệm ép kiểu chuỗi chữ về số thực. Nếu người dùng nhập chữ (VD: 'abc'), lệnh sẽ gãy lập tức
            if num <= 0:
                # ĐIỀU KIỆN LOGIC CỐT LÕI: Nếu số nhỏ hơn hoặc bằng 0, xuất cảnh báo dấu chấm than nguy hiểm
                messagebox.showwarning("Dữ liệu sai quy định", f"Trường '{field_name}' bắt buộc phải là số lớn hơn 0!")
                return None # Trả về rỗng biểu thị kiểm tra thất bại
            return num # Kiểm tra thành công, trả về giá trị số thực sạch sẽ
        except ValueError:
            # Khối ngoại lệ bắt lỗi: Nếu ép kiểu thất bại (người dùng nhập chữ nhầm vào ô số) thì hiện hộp thoại báo lỗi định dạng
            messagebox.showerror("Lỗi định dạng", f"Trường '{field_name}' phải nhập vào định dạng số hợp lệ!")
            return None # Trả về rỗng biểu thị kiểm tra thất bại

    def open_add_dialog(self):
        """Quy trình xử lý hành động Thêm bệnh nhân mới"""
        # Gọi tầng View mở cửa sổ popup con (Toplevel) và thu về các ô nhập dữ liệu cùng nút Lưu thông tin
        win, entries, btn_save = self.view.open_patient_window("Thêm bệnh nhân mới")
        
        def save_action():
            name = entries['name'].get().strip() # Lấy chuỗi họ tên người dùng gõ và cắt bỏ dấu cách thừa ở 2 đầu
            if not name:
                messagebox.showwarning("Cảnh báo dữ liệu", "Họ tên bệnh nhân không được để trống!")
                return # Dừng quy trình nếu bỏ trống tên bện nhân
            
            # Gửi dữ liệu từng ô số qua bộ lọc kiểm tra số thực dương lớn hơn 0
            age_val = self._validate_positive_number(entries['age'].get(), "Tuổi")
            if age_val is None: return # Nếu lỗi, dừng ngay quy trình lưu
            
            weight_val = self._validate_positive_number(entries['weight'].get(), "Cân nặng")
            if weight_val is None: return
            
            height_val = self._validate_positive_number(entries['height'].get(), "Chiều cao")
            if height_val is None: return
            
            visits_val = self._validate_positive_number(entries['visits'].get(), "Số lần khám")
            if visits_val is None: return

            # Sau khi vượt qua tất cả các bài toán validation dữ liệu sạch, tiến hành đóng gói thành Dictionary
            data = {
                'Họ tên': name, 'Tuổi': str(int(age_val)), 'Giới tính': entries['gender'].get(),
                'Cân nặng': str(weight_val), 'Chiều cao': str(height_val), 'Số lần khám': str(int(visits_val))
            }
            
            # Sử dụng hàm pd.concat để chèn dòng hồ sơ mới này vào cuối bảng dữ liệu lớn đang quản lý trong RAM
            self.model.df = pd.concat([self.model.df, pd.DataFrame([data])], ignore_index=True)
            self.model.save()      # Ra lệnh cho Model lưu dữ liệu mới xuống file cứng CSV vĩnh viễn
            self.refresh()         # Tải lại toàn bộ bảng danh sách để cập nhật bệnh nhân mới lên màn hình chính
            win.destroy()          # Giải phóng bộ nhớ và tắt cửa sổ popup nhập liệu đi
            messagebox.showinfo("Thành công", "Đã thêm bệnh nhân thành công!")
            
        btn_save.config(command=save_action) # Gán lệnh thực thi hành động lưu vào nút bấm Lưu của popup

    def open_edit_dialog(self):
        """Quy trình xử lý hành động Sửa đổi hồ sơ thông tin bệnh nhân"""
        sel = self.view.tree.selection() # Lấy ID của dòng mà người dùng đang click chuột chọn trên bảng danh sách
        if not sel: 
            # Xử lý ngoại lệ: Nếu người dùng chưa chọn ai mà đã bấm nút Sửa, hiện cảnh báo nhắc nhở ngay
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng bệnh nhân để sửa!")
            return
        
        # Trích xuất số ID hiển thị của dòng đầu tiên được chọn, trừ đi 1 để tìm ra đúng vị trí dòng index trong mảng Pandas
        display_id = int(self.view.tree.item(sel[0])['values'][0])
        idx = display_id - 1
        
        # Chuyển dòng dữ liệu của bệnh nhân được chọn thành dạng từ điển Dictionary để truyền dữ liệu cũ vào Form popup
        current_data = self.model.df.iloc[idx].to_dict() 
        win, entries, btn_save = self.view.open_patient_window("Chỉnh sửa thông tin bệnh nhân", current_data)
        
        def save_action():
            name = entries['name'].get().strip() # Thu thập tên mới sửa và cắt khoảng trắng rác
            if not name: return
            
            # Tiếp tục ép bộ lọc kiểm tra số thực dương lớn hơn 0 để ngăn chặn người dùng sửa cân nặng/chiều cao thành số âm
            age_val = self._validate_positive_number(entries['age'].get(), "Tuổi")
            if age_val is None: return
            
            weight_val = self._validate_positive_number(entries['weight'].get(), "Cân nặng")
            if weight_val is None: return
            
            height_val = self._validate_positive_number(entries['height'].get(), "Chiều cao")
            if height_val is None: return
            
            visits_val = self._validate_positive_number(entries['visits'].get(), "Số lần khám")
            if visits_val is None: return

            # Sử dụng hàm .at của Pandas để ghi đè trực tiếp các giá trị mới sửa đổi vào đúng tọa độ hàng/cột trên RAM
            self.model.df.at[idx, 'Họ tên'] = name
            self.model.df.at[idx, 'Tuổi'] = str(int(age_val))
            self.model.df.at[idx, 'Giới tính'] = entries['gender'].get()
            self.model.df.at[idx, 'Cân nặng'] = str(weight_val)
            self.model.df.at[idx, 'Chiều cao'] = str(height_val)
            self.model.df.at[idx, 'Số lần khám'] = str(int(visits_val))
            
            self.model.save() # Ghi đè cập nhật mới xuống file cơ sở dữ liệu CSV
            self.refresh()    # Làm mới giao diện hiển thị bảng chính
            win.destroy()     # Tắt popup đi
            messagebox.showinfo("Thành công", "Đã cập nhật thay đổi thành công!")
            
        btn_save.config(command=save_action)

    def show_detail_panel(self, event):
        """Hàm trích xuất hồ sơ liên kết: Khi click chuột chọn dòng nào trên bảng, lập tức dịch toàn bộ hồ sơ chi tiết ra chữ hoa văn bản ở rìa khung dưới"""
        sel = self.view.tree.selection() # Lấy đối tượng dòng được chọn từ chuột
        if not sel or len(sel) > 1: return # Nếu không chọn ai hoặc chọn nhiều người cùng lúc thì thoát hàm
        
        display_id = int(self.view.tree.item(sel[0])['values'][0]) # Tìm vị trí dòng index toán học của Pandas
        idx = display_id - 1
        
        raw_data = self.model.df.iloc[idx] # Trích xuất thông tin gốc dạng chuỗi trong database
        processed_df = self.model.get_processed_data().iloc[idx] # Trích xuất thông tin nâng cao đã qua tính toán toán học
        
        # SỬA LỖI HÌNH 2: Ép kiểu dữ liệu sang chuỗi ký tự bằng hàm str() trước khi gọi hàm viết hoa chữ .upper() để tránh sập app do dính ô trống NaN
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
        # Thay đổi nhãn văn bản ở khung chi tiết để người dùng đọc thông tin hồ sơ y tế trực quan
        self.view.lbl_detail.config(text=detail_text, foreground="#1e272e")

    def delete(self):
        """Quy trình xử lý hành động Xóa bản ghi bệnh nhân khỏi phần mềm"""
        sel = self.view.tree.selection() # Lấy ID dòng chọn
        if not sel: return # KỊCH BẢN KIỂM THỬ HÌNH 4 CÂU 13: Nếu người dùng cố tình bấm xóa khi chưa chọn ai trên bảng, hàm tự thoát bảo vệ hệ thống
        
        display_id = int(self.view.tree.item(sel[0])['values'][0]) # Tìm index dòng dữ liệu thực tế
        idx = display_id - 1
        
        patient_name = self.model.df.iloc[idx]['Họ tên'] # Lấy tên bệnh nhân chuẩn bị xóa để làm thông báo xác nhận
        
        # Xuất hộp thoại lựa chọn Yes/No (Có/Không) hỏi ý kiến người dùng để đề phòng hành động bấm nhầm chuột xóa mất dữ liệu quý
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa bệnh nhân '{patient_name}' không?"):
            # Sử dụng hàm .drop của thư viện Pandas để triệt tiêu dòng dữ liệu tại vị trí index, sau đó reset lại chỉ số mảng liên tục
            self.model.df = self.model.df.drop(idx).reset_index(drop=True)
            self.model.save() # Ghi nhận thay đổi xóa vĩnh viễn xuống file CSV
            self.refresh()    # Vẽ lại bảng dữ liệu mới trên màn hình (bệnh nhân bị xóa sẽ biến mất khỏi bảng)

    def search(self):
        """Thuật toán Tìm kiếm thông minh: Lọc danh sách bệnh nhân gần đúng theo từ khóa bất kỳ"""
        q = self.view.ent_search.get().lower().strip() # Thu thập từ khóa tìm kiếm, chuyển toàn bộ về chữ thường để so sánh không phân biệt hoa thường
        col = self.view.search_col.get() # Xem người dùng đang chọn lọc theo tiêu chí cụ thể nào ở hộp chọn Combobox
        df = self.model.get_processed_data() # Lấy bảng dữ liệu tạm đã qua tính toán BMI để lọc được cả tình trạng sức khỏe
        
        # Thực hiện các mệnh đề rẽ nhánh thuật toán lọc mảng nâng cao của thư viện Pandas dựa trên hàm chứa chuỗi gần đúng .contains()
        if col == "Họ tên": 
            res = df[df['Họ tên'].str.lower().str.contains(q, na=False)]
        elif col == "Nhóm tuổi": 
            res = df[df['Nhóm tuổi'].str.lower().str.contains(q, na=False)]
        elif col == "Giới tính": 
            res = df[df['Giới tính'].str.lower().str.contains(q, na=False)]
        elif col == "Tình trạng SK": 
            res = df[df['Trạng thái hiển thị'].str.lower().str.contains(q, na=False)]
        else: 
            # Trường hợp chọn 'Tất cả': Dùng hàm apply quét quét toàn bộ các ô chữ của mọi cột, chỉ cần 1 ô chứa từ khóa (.any) là giữ lại dòng đó
            res = df[df.apply(lambda r: r.astype(str).str.lower().str.contains(q).any(), axis=1)]
        
        # Xóa sạch bảng Treeview hiển thị hiện tại để chuẩn bị nạp mảng kết quả bộ lọc tìm kiếm mới vào
        for i in self.view.tree.get_children(): self.view.tree.delete(i)
            
        # Vòng lặp đổ các dòng thỏa mãn điều kiện tìm kiếm lên màn hình giao diện chính
        for count, (idx, r) in enumerate(res.iterrows()):
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            self.view.tree.insert("", "end", values=(
                idx + 1, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], 
                r['Nhóm tuổi'], r['Trạng thái hiển thị'], r['Số lần khám']
            ), tags=(row_tag,))

    def import_csv(self):
        """Hành động tích hợp hệ thống: Nạp dữ liệu từ một tệp CSV bên ngoài vào phần mềm"""
        # Gọi hộp thoại hệ thống bắt người dùng chọn tệp tin có đuôi mở rộng bắt buộc là .csv
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            try:
                # Dùng Pandas đọc file CSV ngoài đưa vào RAM cấu trúc mảng tạm thời
                self.model.df = pd.read_csv(path, dtype=str)
                # Tự động loại bỏ cột rác không khớp cấu trúc ứng dụng
                if 'Huyết áp' in self.model.df.columns: self.model.df = self.model.df.drop(columns=['Huyết áp'])
                if 'Số lần khám' not in self.model.df.columns: self.model.df['Số lần khám'] = "1"
                self.model.save() # Lưu dữ liệu hợp nhất mới này đè vào file database nội bộ hệ thống
                self.refresh()    # Làm mới bảng chính
            except Exception: 
                # Bẫy lỗi ngoại lệ: Nếu file CSV bên ngoài bị sai cấu trúc cột hoặc hỏng mã hóa dữ liệu, hiện cảnh báo cấu trúc không tương thích
                messagebox.showerror("Lỗi tệp", "Cấu trúc tệp CSV ngoài không tương thích!")

    def export_csv(self):
        """Hành động xuất bản dữ liệu: Trích xuất và sao lưu bảng dữ liệu hệ thống ra một file CSV lưu ở vị trí bất kỳ trên máy tính"""
        # Gọi hộp thoại lưu file của hệ điều hành, tự động đặt đuôi tệp tin gợi ý mặc định là .csv
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path: 
            # Gọi lệnh xuất dữ liệu của Pandas để trích xuất file Excel phẳng CSV ra vị trí người dùng mong muốn
            self.model.df.to_csv(path, index=False)
            