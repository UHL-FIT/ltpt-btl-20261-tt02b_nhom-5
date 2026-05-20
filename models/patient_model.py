import pandas as pd  # Thư viện xử lý dữ liệu dạng bảng phân tích cao cấp
import os            # Thư viện hệ điều hành - Dùng để kiểm tra và tạo thư mục lưu trữ file

class PatientModel:
    def __init__(self, data_path="data/patients.csv"):
        """
        Khởi tạo Mô hình dữ liệu.
        Xác định đường dẫn lưu trữ file CSV cấu trúc và tự động nạp dữ liệu vào bộ nhớ RAM khi chạy phần mềm.
        """
        self.data_path = data_path
        # Danh sách cấu trúc các cột dữ liệu bắt buộc phải có trong file CSV gốc lưu trên máy tính
        self.columns = ['Họ tên', 'Tuổi', 'Giới tính', 'Cân nặng', 'Chiều cao', 'Huyết áp', 'Số lần khám']
        
        # Tự động tạo thư mục 'data' nếu trên máy tính chưa có thư mục này để tránh lỗi sập phần mềm
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        self._load_data() # Gọi hàm nạp dữ liệu từ file cứng vào RAM

    def _load_data(self):
        """Đọc tệp tin CSV lưu trữ trên máy tính đưa vào DataFrame dữ liệu của thư viện Pandas"""
        if os.path.exists(self.data_path):
            try: 
                # Đọc file CSV, quy định mọi dữ liệu thô đều là chuỗi (string) để tối ưu bẫy lỗi ở Controller
                self.df = pd.read_csv(self.data_path, dtype=str)
                
                # Sửa đổi đồng bộ tên cột nếu có sự sai lệch cấu trúc cũ
                if 'Tình trạng sức khỏe' in self.df.columns:
                    self.df = self.df.rename(columns={'Tình trạng sức khỏe': 'Huyết áp'})
                    
                # Vòng lặp kiểm tra: Nếu thiếu bất kỳ cột chuẩn nào thì tự động tạo cột trống đó ra để bảo vệ logic phần mềm
                for col in self.columns:
                    if col not in self.df.columns:
                        self.df[col] = "1" if col == "Số lần khám" else ""
            except: 
                # Nếu file CSV bị lỗi cấu trúc nặng, tạo mới một bảng trống hoàn toàn dựa trên khung cột chuẩn
                self.df = pd.DataFrame(columns=self.columns)
        else:
            # Nếu chạy phần mềm lần đầu và chưa có file CSV nào, tự khởi tạo bảng dữ liệu trống
            self.df = pd.DataFrame(columns=self.columns)

    def calculate_bmi(self, weight, height):
        """
        [THUẬT TOÁN CỐT LÕI 1]: Tính chỉ số khối cơ thể BMI.
        Công thức y học: BMI = Cân nặng (kg) / Chiều cao^2 (m).
        """
        try:
            w, h = float(weight), float(height)
            # BẪY TỰ ĐỘNG QUY ĐỔI ĐƠN VỊ: Nếu người dùng nhập đơn vị cm (Ví dụ: 170), thuật toán tự đổi sang mét (1.7)
            if h > 3:  
                h = h / 100
            # Trả về chỉ số BMI làm tròn lấy 2 số sau dấu phẩy thập phân. Nếu chiều cao bằng 0 thì trả về 0 để tránh lỗi chia cho 0
            return round(w / (h ** 2), 2) if h > 0 else 0
        except: 
            # Phòng ngừa trường hợp dữ liệu đầu vào không phải là số hợp lệ, trả về 0 bảo vệ logic hệ thống
            return 0  

    def get_age_group(self, age):
        """
        [THUẬT TOÁN CỐT LÕI 2]: Phân loại nhóm tuổi bệnh nhân dựa theo số tuổi sinh học.
        """
        try:
            a = int(float(age)) # Ép kiểu dữ liệu về số nguyên
            if a < 30: 
                return 'Thanh niên'
            elif a <= 50: 
                return 'Trung niên'
            return 'Người cao tuổi'
        except: 
            return 'N/A' # Trả về không xác định nếu dữ liệu đầu vào bị lỗi

    def get_health_status(self, bp_string):
        """
        [THUẬT TOÁN CỐT LÕI 3]: Phân tích chỉ số Huyết áp và phân loại trạng thái lâm sàng.
        Hỗ trợ đọc cả dạng số đơn (120) và dạng phân số Tâm thu/Tâm trương chuẩn y khoa (120/80).
        """
        try:
            bp_string = str(bp_string).strip()
            if not bp_string or bp_string.lower() == "nan":
                return "Chưa rõ"
                
            # Trường hợp 1: Người dùng nhập dạng số đơn lẻ (Ví dụ: 125)
            if '/' not in bp_string:
                systolic = float(bp_string) # Lấy chỉ số huyết áp tâm thu
                if systolic >= 140: return "Huyết áp cao"
                elif systolic < 90: return "Huyết áp thấp"
                return "Ổn định"
            
            # Trường hợp 2: Người dùng nhập dạng chuẩn y khoa có gạch chéo phân tách (Ví dụ: 120/80)
            # Sử dụng hàm map và split để tách chuỗi thành 2 số thực: Huyết áp tâm thu và Huyết áp tâm trương
            systolic, diastolic = map(float, bp_string.split('/'))
            if systolic >= 140 or diastolic >= 90:
                return "Huyết áp cao"
            elif systolic < 90 or diastolic < 60:
                return "Huyết áp thấp"
            else:
                return "Ổn định"
        except:
            return "Ổn định" # Mặc định trả về ổn định nếu có lỗi định dạng ngoài ý muốn xảy ra

    def get_processed_data(self):
        """
        HÀM XỬ LÝ DỮ LIỆU ĐẦU RA (Tạo cột ảo):
        Nhân bản bảng dữ liệu gốc, chạy các thuật toán để sinh thêm 3 cột tính toán động: BMI, Nhóm tuổi, Tình trạng SK
        để phục vụ hiển thị lên Treeview mà không làm biến đổi file CSV gốc.
        """
        temp_df = self.df.copy() # Tạo một bản sao độc lập của DataFrame để xử lý nội bộ
        if not temp_df.empty:
            # Sử dụng hàm .apply(lambda) của Pandas để chạy thuật toán tính BMI tự động cho từng dòng dữ liệu trong bảng
            temp_df['BMI'] = temp_df.apply(lambda x: self.calculate_bmi(x['Cân nặng'], x['Chiều cao']), axis=1)
            # Sử dụng hàm .apply() để ánh xạ thuật toán phân nhóm tuổi và trạng thái huyết áp cho toàn cột tương ứng
            temp_df['Nhóm tuổi'] = temp_df['Tuổi'].apply(self.get_age_group)
            temp_df['Trạng thái hiển thị'] = temp_df['Huyết áp'].apply(self.get_health_status)
            temp_df['Số lần khám'] = temp_df['Số lần khám'].fillna(1).astype(int) # Điền số 1 nếu ô số lần khám bị bỏ trống
        else:
            # Khởi tạo các cột ảo dạng rỗng nếu bảng gốc chưa có bệnh nhân nào
            temp_df['BMI'] = None
            temp_df['Nhóm tuổi'] = None
            temp_df['Trạng thái hiển thị'] = None
        return temp_df

    def save(self):
        """Ghi đè và lưu lại toàn bộ bảng DataFrame hiện hành trong RAM xuống file CSV cứng trên máy tính"""
        self.df.to_csv(self.data_path, index=False)
