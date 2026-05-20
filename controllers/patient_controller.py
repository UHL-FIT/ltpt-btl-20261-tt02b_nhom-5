from tkinter import messagebox, filedialog
import pandas as pd
import re  # Thư viện Regular Expression - Dùng để kiểm tra định dạng chuỗi nâng cao

class PatientController:
    def __init__(self, model, view):
        """
        Hàm khởi tạo (Constructor) của Controller.
        Nhiệm vụ: Liên kết thực thể Model và View lại với nhau.
        """
        self.model = model
        self.view = view
        self._bind_events() # Gọi hàm kích hoạt các bộ lắng nghe sự kiện nút bấm
        self.refresh()      # Tự động đổ dữ liệu lên bảng Treeview ngay khi vừa bật ứng dụng

    def _bind_events(self):
        """
        Hàm kết nối hành động (Event Binding).
        Gắn các nút bấm từ View (.config) với các hàm xử lý logic tương ứng nằm trong Controller.
        """
        self.view.btn_about.config(command=self.show_about)
        self.view.btn_stats.config(command=self.show_stats)
        self.view.btn_add.config(command=self.open_add_dialog)
        self.view.btn_update.config(command=self.open_edit_dialog)
        self.view.btn_delete.config(command=self.delete)
        self.view.btn_search.config(command=self.search)
        self.view.btn_clear.config(command=self.refresh)
        self.view.btn_import.config(command=self.import_csv)
        self.view.btn_export.config(command=self.export_csv)
        
        # [SỰ KIỆN CLICK DÒNG]: Lắng nghe tín hiệu khi người dùng click chuột chọn 1 hàng trên Treeview
        # <<TreeviewSelect>> là sự kiện mặc định của Tkinter phát ra khi dòng được chọn thay đổi.
        self.view.tree.bind("<<TreeviewSelect>>", self.show_detail_panel)

    def show_about(self):
        """Hiển thị hộp thoại thông tin giới thiệu thành viên nhóm phát triển phần mềm"""
        messagebox.showinfo("Giới thiệu", "Nhóm 5 - UHL FIT\nPhần mềm Quản lý Hồ sơ Bệnh nhân nâng cao.")

    def show_stats(self):
        """
        XỬ LÝ LOGIC THỐNG KÊ (Yêu cầu bắt buộc của đề bài):
        Sử dụng hàm gom nhóm nâng cao .groupby() của Pandas để tính toán thông số y khoa.
        """
        df = self.model.get_processed_data() # Lấy DataFrame đã tính sẵn cột ảo (BMI, Nhóm tuổi)
        if df.empty: 
            return # Nếu bảng không có dữ liệu thì dừng hàm, không tính toán tiếp
            
        # Thống kê: Gom nhóm bệnh nhân theo 'Nhóm tuổi', lọc lấy cột 'BMI' và tính trung bình cộng (.mean)
        # observed=False giúp giữ cấu trúc nhóm ổn định, .round(2) để làm tròn 2 chữ số thập phân.
        res = df.groupby('Nhóm tuổi', observed=False)['BMI'].mean().round(2)
        
        # Chuyển kết quả Series của Pandas thành dạng chuỗi văn bản sạch (.to_string) để đưa vào hộp thoại
        messagebox.showinfo("Thống kê BMI", f"Trung bình BMI theo nhóm tuổi:\n\n{res.to_string()}")

    def refresh(self):
        """
        HÀM LÀM MỚI TOÀN BỘ GIAO DIỆN CHÍNH:
        Xóa sạch dữ liệu cũ hiển thị sai lệch, đồng bộ lại dữ liệu mới nhất từ file CSV lên Treeview.
        """
        self.view.ent_search.delete(0, 'end') # Dọn sạch chữ đang nhập dở ở ô tìm kiếm
        df = self.model.get_processed_data()  # Gọi Model cấp bộ dữ liệu mới nhất trong file cứng
        
        # Thiết lập lại khung thông tin chi tiết ở phía dưới về trạng thái chờ ban đầu
        self.view.lbl_detail.config(text="Chưa chọn bệnh nhân nào từ danh sách bảng.", foreground="#57606f")
        
        # Vòng lặp xóa sạch mọi dòng cũ đang hiện trên Treeview để chuẩn bị vẽ lại từ đầu
        for i in self.view.tree.get_children(): 
            self.view.tree.delete(i) 
            
        # Vòng lặp duyệt qua từng hàng (Row) trong bảng dữ liệu DataFrame của Pandas
        # enumerate giúp vừa lấy chỉ số index thực tế (idx), vừa sinh ra biến đếm tự tăng (count)
        for count, (idx, r) in enumerate(df.iterrows()):
            # Thuật toán đổ màu xen kẽ: Nếu dòng chẵn (count % 2 == 0) gắn tag evenrow, ngược lại gắn oddrow
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            
            # Chèn dòng vào Treeview của View. 
            # Đề bài yêu cầu ID hiển thị bắt đầu từ 1, nên ta lấy chỉ số index gốc cộng thêm 1 (idx + 1)
            self.view.tree.insert("", "end", values=(
                idx + 1, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], 
                r['Nhóm tuổi'], r['Trạng thái hiển thị'], r['Số lần khám']
            ), tags=(row_tag,))

    def open_add_dialog(self):
        """Hành động xử lý khi người dùng ấn nút 'Thêm bệnh nhân mới'"""
        # Gọi View mở một cửa sổ popup nhập liệu mới, nhận về các ô nhập dữ liệu (entries) và nút Lưu
        win, entries, btn_save = self.view.open_patient_window("Thêm bệnh nhân mới")
        
        def save_action():
            """Hàm nội bộ chạy khi người dùng ấn nút 'Lưu thông tin' trên Form thêm mới"""
            # [BẪY LỖI TRỐNG HỌ TÊN]: .get() lấy chữ, .strip() cắt bỏ khoảng trắng thừa ở 2 đầu
            if not entries['name'].get().strip():
                messagebox.showwarning("Cảnh báo dữ liệu", "Họ tên bệnh nhân không được để trống!")
                return # Ngắt hàm ngay lập tức, không cho phép lưu xuống file

            # [BẪY LỖI ĐỊNH DẠNG HUYẾT ÁP]: Ép buộc nhập định dạng số thông qua hàm kiểm tra bằng Regex
            bp_val = entries['bp'].get().strip()
            if not self._validate_blood_pressure(bp_val):
                messagebox.showwarning("Cảnh báo dữ liệu", "Huyết áp phải nhập định dạng số (Ví dụ: 120 hoặc 120/80)!")
                return

            try:
                # [BẪY LỖI ÉP KIỂU SỐ LOGIC]: Thử ép kiểu dữ liệu từ chuỗi sang Số nguyên/Số thực.
                # Nếu người dùng cố tình nhập chữ (Ví dụ Tuổi nhập là 'abc'), Python sẽ quăng lỗi ValueError.
                int(entries['age'].get())
                float(entries['weight'].get())
                float(entries['height'].get())
                int(entries['visits'].get())
                
                # Gom toàn bộ dữ liệu hợp lệ trên Form thành một đối tượng từ điển (Dictionary)
                data = {
                    'Họ tên': entries['name'].get().strip(),
                    'Tuổi': entries['age'].get(),
                    'Giới tính': entries['gender'].get(),
                    'Cân nặng': entries['weight'].get(),
                    'Chiều cao': entries['height'].get(),
                    'Huyết áp': bp_val,
                    'Số lần khám': entries['visits'].get()
                }
                
                # Nối dòng dữ liệu từ điển mới này vào đuôi của bảng DataFrame hiện tại
                self.model.df = pd.concat([self.model.df, pd.DataFrame([data])], ignore_index=True)
                self.model.save()      # Ra lệnh cho Model ghi đè mảng dữ liệu mới xuống file CSV cứng
                self.refresh()         # Gọi hàm vẽ lại bảng chính để người dùng thấy dòng mới vừa thêm
                win.destroy()          # Đóng (Tắt) cửa sổ popup nhập liệu
                messagebox.showinfo("Thành công", "Đã thêm bệnh nhân thành công!")
            except ValueError:
                # Trình xử lý ngoại lệ khi các ô dữ liệu kiểu số bị nhập sai định dạng
                messagebox.showerror("Lỗi dữ liệu", "Vui lòng nhập đúng định dạng số cho các ô: Tuổi, Cân nặng, Chiều cao, Số lần khám!")
        
        # Gắn hàm xử lý vừa viết ở trên vào nút Lưu của cửa sổ con
        btn_save.config(command=save_action)

    def open_edit_dialog(self):
        """Hành động xử lý khi người dùng ấn nút 'Sửa thông tin chọn'"""
        sel = self.view.tree.selection() # Lấy danh sách các dòng đang được bôi đen trên Treeview
        
        # [BẪY LỖI CHƯA CHỌN]: Người dùng chưa chọn bất kỳ bệnh nhân nào mà đã ấn nút Sửa
        if not sel: 
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng bệnh nhân từ danh sách để sửa!")
            return
            
        # [BẪY LỖI CHỌN NHIỀU NGƯỜI]: Người dùng dùng phím Ctrl bôi đen nhiều dòng cùng lúc
        if len(sel) > 1:
            messagebox.showerror("Lỗi thao tác", 
                                 "Hệ thống chỉ cho phép chỉnh sửa thông tin của từng bệnh nhân một.\n"
                                 "Vui lòng không chọn nhiều người cùng lúc!")
            return 
            
        # Trường hợp hợp lệ: Chỉ chọn duy nhất 1 bệnh nhân
        # Lấy giá trị của cột ID hiển thị trên bảng (Cột số 0), ép về số nguyên, trừ đi 1 để ra chỉ số index mảng Pandas gốc
        display_id = int(self.view.tree.item(sel[0])['values'][0])
        idx = display_id - 1
        
        # Lấy thông tin thô của dòng đó từ Model, chuyển thành Dictionary
        current_data = self.model.df.iloc[idx].to_dict() 
        # Mở popup nhập liệu, truyền thêm dữ liệu cũ (current_data) để View tự động điền sẵn vào các ô
        win, entries, btn_save = self.view.open_patient_window("Chỉnh sửa thông tin bệnh nhân", current_data)
        
        def save_action():
            """Hàm nội bộ chạy khi người dùng ấn nút 'Lưu thông tin' trên Form chỉnh sửa"""
            # Bẫy lỗi để trống tên khi sửa thông tin
            if not entries['name'].get().strip():
                messagebox.showwarning("Cảnh báo dữ liệu", "Họ tên bệnh nhân không được để trống!")
                return

            # Bẫy lỗi nhập sai định dạng số của huyết áp khi sửa thông tin
            bp_val = entries['bp'].get().strip()
            if not self._validate_blood_pressure(bp_val):
                messagebox.showwarning("Cảnh báo dữ liệu", "Huyết áp phải nhập định dạng số (Ví dụ: 120 hoặc 120/80)!")
                return

            try:
                # Bẫy lỗi ép kiểu số cho các trường dữ liệu đo lường vật lý
                int(entries['age'].get())
                float(entries['weight'].get())
                float(entries['height'].get())
                int(entries['visits'].get())
                
                # Sử dụng thuộc tính .at[vị_trí_dòng, 'tên_cột'] của thư viện Pandas để sửa đè trực tiếp ô dữ liệu trong bộ nhớ
                self.model.df.at[idx, 'Họ tên'] = entries['name'].get().strip()
                self.model.df.at[idx, 'Tuổi'] = entries['age'].get()
                self.model.df.at[idx, 'Giới tính'] = entries['gender'].get()
                self.model.df.at[idx, 'Cân nặng'] = entries['weight'].get()
                self.model.df.at[idx, 'Chiều cao'] = entries['height'].get()
                self.model.df.at[idx, 'Huyết áp'] = bp_val
                self.model.df.at[idx, 'Số lần khám'] = entries['visits'].get()
                
                self.model.save() # Lưu lại mảng dữ liệu mới xuống tệp CSV cứng
                self.refresh()    # Vẽ lại bảng chính với thông tin mới vừa sửa
                win.destroy()     # Đóng popup con
                messagebox.showinfo("Thành công", "Đã cập nhật thay đổi thành công!")
            except ValueError:
                messagebox.showerror("Lỗi dữ liệu", "Kiểm tra định dạng các trường dữ liệu kiểu số!")
                
        btn_save.config(command=save_action)

    def show_detail_panel(self, event):
        """
        [HÀM XỬ LÝ SỰ KIỆN LẮNG NGHE CHUỘT]:
        Hàm tự động chạy mỗi khi người dùng click chuột trái chọn một hàng trên bảng Treeview.
        Giải thích tham số 'event': Biến chứa thông tin sự kiện click chuột của Tkinter truyền vào.
        """
        sel = self.view.tree.selection() # Trích xuất dòng đang chọn
        if not sel or len(sel) > 1:
            return # Nếu click trượt hoặc chọn nhiều người thì thoát hàm, không hiển thị gì cả

        # Tính toán vị trí dòng dựa theo ID hiển thị
        display_id = int(self.view.tree.item(sel[0])['values'][0])
        idx = display_id - 1

        # Lấy dữ liệu thô (raw) trong file CSV và dữ liệu ảo đã tính toán (processed) của bệnh nhân đó
        raw_data = self.model.df.iloc[idx]
        processed_df = self.model.get_processed_data().iloc[idx]

        # Xây dựng chuỗi văn bản mẫu (Formatted String) nối các thông số bệnh án rõ ràng, khoa học
        detail_text = (
            f"👤 Họ và tên: {raw_data['Họ tên'].upper()}  |  "
            f"🎂 Tuổi: {raw_data['Tuổi']} ({processed_df['Nhóm tuổi']})  |  "
            f"⚥ Giới tính: {raw_data['Giới tính']}\n"
            f"⚖️ Cân nặng: {raw_data['Cân nặng']} kg  |  "
            f"📏 Chiều cao: {raw_data['Chiều cao']} cm  |  "
            f"📈 Chỉ số BMI: {processed_df['BMI']}  |  "
            f"❤️ Huyết áp gốc: {raw_data['Huyết áp']} mmHg ({processed_df['Trạng thái hiển thị']})  |  "
            f"🏥 Số lần khám: {processed_df['Số lần khám']} lần"
        )
        
        # Đổ văn bản chi tiết lên thanh nhãn Label nằm trong Khu vực 4 của View, đổi màu chữ sang màu đậm dễ nhìn
        self.view.lbl_detail.config(text=detail_text, foreground="#1e272e")

    def _validate_blood_pressure(self, bp_string):
        """
        Hàm bổ trợ (Helper function) dùng biểu thức chính quy (Regex) kiểm tra tính hợp lệ của Huyết áp.
        Quy tắc: Chuỗi không trống, chỉ chứa các chữ số, chấp nhận dấu gạch chéo phân cách.
        Ví dụ hợp lệ: '120', '120/80'. Ví dụ không hợp lệ: '120a', 'abc', '120/80/90'.
        """
        if not bp_string:
            return False
        # Chuỗi mẫu Regex: ^ (bắt đầu), \d+ (một hoặc nhiều số), (\/\d+)? (có thể có hoặc không cụm /số), $ (kết thúc)
        pattern = r"^\d+(\/\d+)?$"
        return bool(re.match(pattern, bp_string))

    def delete(self):
        """Hành động xử lý khi bấm nút 'Xóa bệnh nhân'"""
        sel = self.view.tree.selection()
        if not sel: 
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return
            
        # Hiển thị hộp thoại Hỏi Xác nhận dạng Yes/No phòng trường hợp người dùng click nhầm nút Xóa
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bệnh nhân này không?"):
            display_id = int(self.view.tree.item(sel[0])['values'][0])
            idx = display_id - 1
            # Sử dụng lệnh .drop(idx) của Pandas để xóa hàng tại vị trí chỉ định
            # .reset_index(drop=True) để thiết lập lại chỉ số mảng liên tục từ 0, tránh bị đứt gãy chỉ số sau khi xóa
            self.model.df = self.model.df.drop(idx).reset_index(drop=True)
            self.model.save() # Lưu lại file CSV sau khi xóa dữ liệu thành công
            self.refresh()    # Làm mới lại bảng chính

    def search(self):
        """
        THUẬT TOÁN TÌM KIẾM NÂNG CAO (Bộ lọc thông minh theo từng cột được chỉ định):
        Sử dụng cơ chế lọc mảng Boolean Series của Pandas kết hợp hàm xử lý chuỗi `.str.contains()`.
        """
        q = self.view.ent_search.get().lower().strip() # Lấy từ khóa tìm kiếm, chuyển thành chữ thường, cắt khoảng trắng
        df = self.model.get_processed_data()          # Lấy bảng dữ liệu đầy đủ các cột tính toán để quét bộ lọc
        col = self.view.search_col.get()               # Đọc tên cột người dùng đang chọn trên thanh Combobox lọc
        
        # Tiến hành ép cột cần lọc về chữ thường (.str.lower) và quét xem có chứa từ khóa không (.str.contains)
        if col == "Họ tên": 
            res = df[df['Họ tên'].str.lower().str.contains(q, na=False)]
        elif col == "Nhóm tuổi": 
            res = df[df['Nhóm tuổi'].str.lower().str.contains(q, na=False)]
        elif col == "Giới tính":
            res = df[df['Giới tính'].str.lower().str.contains(q, na=False)]
        elif col == "Tình trạng SK":
            res = df[df['Trạng thái hiển thị'].str.lower().str.contains(q, na=False)]
        else: 
            # Trường hợp chọn 'Tất cả': Dùng hàm lambda quét qua mọi ô dữ liệu trong dòng (axis=1) để tìm từ khóa thích hợp
            res = df[df.apply(lambda r: r.astype(str).str.lower().str.contains(q).any(), axis=1)]
        
        # Xóa sạch bảng cũ và vẽ lại bảng mới chỉ hiển thị các dòng khớp với kết quả tìm kiếm (res)
        for i in self.view.tree.get_children(): 
            self.view.tree.delete(i)
        for count, (idx, r) in enumerate(res.iterrows()):
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            self.view.tree.insert("", "end", values=(
                idx + 1, r['Họ tên'], r['Tuổi'], r['Giới tính'], r['BMI'], 
                r['Nhóm tuổi'], r['Trạng thái hiển thị'], r['Số lần khám']
            ), tags=(row_tag,))

    def import_csv(self):
        """Hàm mở hộp thoại hệ điều hành để người dùng chọn tệp tin CSV bên ngoài nạp vào app"""
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            # Đọc file CSV bằng Pandas, ép mọi cột về dạng chữ (dtype=str) để tránh mất số 0 ở đầu dữ liệu
            self.model.df = pd.read_csv(path, dtype=str)
            
            # Chuẩn hóa dữ liệu nâng cao: Nếu file cũ chứa tiêu đề tên khác, tự động đổi tên cột cho đồng bộ cấu trúc phần mềm
            if 'Tình trạng sức khỏe' in self.model.df.columns:
                self.model.df = self.model.df.rename(columns={'Tình trạng sức khỏe': 'Huyết áp'})
            if 'Số lần khám' not in self.model.df.columns:
                self.model.df['Số lần khám'] = "1" # Tự động bù dữ liệu nếu cột bị thiếu hụt
                
            self.model.save()   # Lưu bộ dữ liệu mới nạp này vào file CSV hệ thống
            self.refresh()      # Làm mới giao diện

    def export_csv(self):
        """Hàm mở hộp thoại của hệ điều hành cho người dùng chọn thư mục và đặt tên file để trích xuất dữ liệu ra tệp CSV riêng"""
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path: 
            # Ghi dữ liệu DataFrame ra tệp tin, index=False để loại bỏ cột chỉ số mặc định của Pandas khỏi file xuất ra
            self.model.df.to_csv(path, index=False)
