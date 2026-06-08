import pandas as pd  # Thư viện Pandas: Dùng để thao tác và xử lý dữ liệu dạng bảng (DataFrame)
import os            # Thư viện OS: Dùng để làm việc với hệ thống tệp tin và thư mục của máy tính
from utils.logger import setup_logger # Hàm tự dựng để khởi tạo hệ thống ghi log lịch sử chạy phần mềm

class PatientModel:
    def __init__(self, data_path="data/patients.csv"):
        # Đường dẫn tới tệp tin CSV dùng làm cơ sở dữ liệu lưu trữ hồ sơ bệnh nhân
        self.data_path = data_path
        
        # Định nghĩa danh sách các tiêu đề cột chuẩn có trong tệp tin database CSV
        self.columns = ['Họ tên', 'Tuổi', 'Giới tính', 'Cân nặng', 'Chiều cao', 'Số lần khám']
        
        # Khởi tạo đối tượng logger riêng cho tầng Model để ghi nhận lỗi hoặc lịch sử nạp dữ liệu
        self.logger = setup_logger("patient_model")
        
        # Biến cờ (Flag) dùng để đảo chiều sắp xếp: True là từ A-Z, False là từ Z-A
        self.sort_ascending = True 
        
        # Lệnh kiểm tra và tự động tạo thư mục 'data' nếu thư mục này chưa tồn tại trên máy tính
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        
        # Gọi hàm nội bộ để bắt đầu đọc dữ liệu từ file CSV lên bộ nhớ RAM khi phần mềm khởi động
        self._load_data()

    def _load_data(self):
        """Hàm nội bộ: Đọc dữ liệu từ ổ cứng (file CSV) nạp vào bộ nhớ RAM"""
        if os.path.exists(self.data_path):
            try: 
                # Đọc tệp CSV. Tham số dtype=str ép tất cả dữ liệu thành chuỗi chữ để tránh lỗi định dạng tự động
                self.df = pd.read_csv(self.data_path, dtype=str)
                
                # Chuẩn hóa dữ liệu: Loại bỏ cột 'Huyết áp' cũ nếu file CSV cũ còn sót lại cột này
                if 'Huyết áp' in self.df.columns:
                    self.df = self.df.drop(columns=['Huyết áp'])
                
                # Chuẩn hóa dữ liệu: Loại bỏ cột 'Tình trạng sức khỏe' tĩnh để chuyển sang tính toán động
                if 'Tình trạng sức khỏe' in self.df.columns:
                    self.df = self.df.drop(columns=['Tình trạng sức khỏe'])
                
                # Vòng lặp kiểm tra: Nếu thiếu bất kỳ cột chuẩn nào, tự động bù cột đó vào bảng dữ liệu
                for col in self.columns:
                    if col not in self.df.columns:
                        # Nếu là cột số lần khám thì điền mặc định là "1", các cột khác để trống ""
                        self.df[col] = "1" if col == "Số lần khám" else ""
                        
                self.logger.info(f"Nạp cơ sở dữ liệu thành công ({len(self.df)} dòng).")
            except Exception as e: 
                # Trường hợp file CSV bị lỗi cấu trúc nghiêm trọng, ghi log lỗi và khởi tạo bảng trống
                self.logger.error(f"Lỗi đọc file CSV: {str(e)}")
                self.df = pd.DataFrame(columns=self.columns)
        else:
            # Nếu phần mềm chạy lần đầu và chưa có file CSV, tự động tạo một bảng trống hoàn toàn
            self.df = pd.DataFrame(columns=self.columns)

    def sort_by_name(self):
        """Thuật toán sắp xếp danh sách bệnh nhân theo thứ tự bảng chữ cái Họ tên"""
        if self.df.empty: return # Nếu bảng dữ liệu đang trống thì không làm gì cả
        
        # Gọi hàm sort_values của Pandas để sắp xếp mảng dựa trên cột 'Họ tên'
        self.df = self.df.sort_values(by='Họ tên', ascending=self.sort_ascending).reset_index(drop=True)
        
        # Đảo ngược giá trị biến cờ để lần nhấp đúp chuột tiếp theo sẽ sắp xếp theo chiều ngược lại
        self.sort_ascending = not self.sort_ascending

    def calculate_bmi(self, weight, height):
        """Thuật toán y khoa: Tính chỉ số khối cơ thể BMI từ Cân nặng (kg) và Chiều cao (cm/m)"""
        try:
            w, h = float(weight), float(height) # Ép kiểu dữ liệu từ chuỗi chữ sang số thực
            if h > 3: h = h / 100 # Nếu người dùng nhập chiều cao dạng cm (VD: 170), tự động quy đổi về mét (1.7)
            
            # Công thức chuẩn y khoa: BMI = Cân nặng / (Chiều cao bình phương). Làm tròn lấy 2 chữ số thập phân.
            return round(w / (h ** 2), 2) if h > 0 else 0
        except: 
            return 0 # Trả về điểm 0 nếu dữ liệu truyền vào bị lỗi toán học hoặc không phải số

    def get_age_group(self, age):
        """Thuật toán phân loại nhóm tuổi phục vụ công tác thống kê y tế"""
        try:
            a = int(float(age)) # Ép dữ liệu tuổi về dạng số nguyên
            if a < 30: return 'Thanh niên'
            elif a <= 50: return 'Trung niên'
            return 'Người cao tuổi' # Trên 50 tuổi xếp vào nhóm người cao tuổi
        except: 
            return 'N/A' # Trả về không xác định nếu ô dữ liệu tuổi bị lỗi dữ liệu

    def get_bmi_status(self, bmi_value):
        """Thuật toán phân loại thể trạng sức khỏe dựa trên điểm số BMI theo tiêu chuẩn Châu Á IDI&WPRO"""
        if bmi_value <= 0: return "Chưa rõ"
        if bmi_value < 18.5: return "Thiếu cân (Gầy)"
        elif bmi_value < 23.0: return "Bình thường"
        elif bmi_value < 25.0: return "Thừa cân"
        else: return "Béo phì" # Mọi trường hợp BMI từ 25.0 trở lên đều là béo phì

    def get_processed_data(self):
        """Hàm xử lý dữ liệu động: Tạo bảng tạm thời chứa đầy đủ các cột tính toán nâng cao để hiển thị lên giao diện"""
        temp_df = self.df.copy() # Sao chép bảng gốc ra một bảng tạm trên RAM nhằm giữ an toàn dữ liệu gốc
        
        if not temp_df.empty:
            # Ứng dụng hàm lambda để duyệt qua từng dòng, tự động tính chỉ số BMI động cho từng bệnh nhân
            temp_df['BMI'] = temp_df.apply(lambda x: self.calculate_bmi(x['Cân nặng'], x['Chiều cao']), axis=1)
            
            # Sử dụng hàm apply để quét cột Tuổi và tự sinh ra giá trị phân loại Nhóm tuổi tương ứng
            temp_df['Nhóm tuổi'] = temp_df['Tuổi'].apply(self.get_age_group)
            
            # Sử dụng hàm apply để quét cột BMI vừa tính và tự sinh ra văn bản Tình trạng sức khỏe tương ứng
            temp_df['Trạng thái hiển thị'] = temp_df['BMI'].apply(self.get_bmi_status)
            
            # Chuẩn hóa dữ liệu: Xử lý các ô trống ở cột Số lần khám, ép về kiểu số nguyên (int) để hiển thị đẹp mắt
            temp_df['Số lần khám'] = temp_df['Số lần khám'].fillna(1).astype(int)
        else:
            # Nếu bảng trống, gán giá trị None cho các cột kỹ thuật để tránh gây lỗi hệ thống
            temp_df['BMI'] = None; temp_df['Nhóm tuổi'] = None; temp_df['Trạng thái hiển thị'] = None
            
        return temp_df # Trả về bảng kết quả đã được tính toán xử lý đầy đủ thông tin

    def save(self):
        """Hàm lưu trữ vĩnh viễn: Ghi toàn bộ dữ liệu hiện hành trên RAM xuống file cứng CSV"""
        try: 
            # Ghi bảng DataFrame xuống file CSV. index=False nghĩa là bỏ qua không lưu cột số thứ tự ẩn của Pandas
            self.df.to_csv(self.data_path, index=False)
        except Exception as e: 
            # Ghi log cảnh báo mức độ tối cao nếu ổ cứng bị khóa hoặc phần mềm không có quyền ghi file
            self.logger.critical(f"Lỗi nghiêm trọng không thể ghi file CSV: {str(e)}")
