import pandas as pd  
import os            
from utils.logger import setup_logger

class PatientModel:
    def __init__(self, data_path="data/patients.csv"):
        self.data_path = data_path
        self.columns = ['Họ tên', 'Tuổi', 'Giới tính', 'Cân nặng', 'Chiều cao', 'Số lần khám']
        self.logger = setup_logger("patient_model")
        self.sort_ascending = True 
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            try: 
                self.df = pd.read_csv(self.data_path, dtype=str)
                if 'Huyết áp' in self.df.columns:
                    self.df = self.df.drop(columns=['Huyết áp'])
                if 'Tình trạng sức khỏe' in self.df.columns:
                    self.df = self.df.drop(columns=['Tình trạng sức khỏe'])
                for col in self.columns:
                    if col not in self.df.columns:
                        self.df[col] = "1" if col == "Số lần khám" else ""
                self.logger.info(f"Nạp cơ sở dữ liệu thành công ({len(self.df)} dòng).")
            except Exception as e: 
                self.logger.error(f"Lỗi đọc file CSV: {str(e)}")
                self.df = pd.DataFrame(columns=self.columns)
        else:
            self.df = pd.DataFrame(columns=self.columns)

    def sort_by_name(self):
        if self.df.empty: return
        self.df = self.df.sort_values(by='Họ tên', ascending=self.sort_ascending).reset_index(drop=True)
        self.sort_ascending = not self.sort_ascending

    def calculate_bmi(self, weight, height):
        try:
            w, h = float(weight), float(height)
            if h > 3: h = h / 100
            return round(w / (h ** 2), 2) if h > 0 else 0
        except: return 0  

    def get_age_group(self, age):
        try:
            a = int(float(age))
            if a < 30: return 'Thanh niên'
            elif a <= 50: return 'Trung niên'
            return 'Người cao tuổi'
        except: return 'N/A'

    def get_bmi_status(self, bmi_value):
        if bmi_value <= 0: return "Chưa rõ"
        if bmi_value < 18.5: return "Thiếu cân (Gầy)"
        elif bmi_value < 23.0: return "Bình thường"
        elif bmi_value < 25.0: return "Thừa cân"
        else: return "Béo phì"

    def get_processed_data(self):
        temp_df = self.df.copy() 
        if not temp_df.empty:
            temp_df['BMI'] = temp_df.apply(lambda x: self.calculate_bmi(x['Cân nặng'], x['Chiều cao']), axis=1)
            temp_df['Nhóm tuổi'] = temp_df['Tuổi'].apply(self.get_age_group)
            temp_df['Trạng thái hiển thị'] = temp_df['BMI'].apply(self.get_bmi_status)
            temp_df['Số lần khám'] = temp_df['Số lần khám'].fillna(1).astype(int)
        else:
            temp_df['BMI'] = None; temp_df['Nhóm tuổi'] = None; temp_df['Trạng thái hiển thị'] = None
        return temp_df

    def save(self):
        try: self.df.to_csv(self.data_path, index=False)
        except Exception as e: self.logger.critical(f"Lỗi ghi file CSV: {str(e)}")
