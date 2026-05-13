import pandas as pd
import os

class PatientModel:
    def __init__(self, data_path="data/patients.csv"):
        self.data_path = data_path
        self.columns = ['Họ tên', 'Tuổi', 'Giới tính', 'Cân nặng', 'Chiều cao', 'Huyết áp']
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            try: self.df = pd.read_csv(self.data_path)
            except: self.df = pd.DataFrame(columns=self.columns)
        else:
            self.df = pd.DataFrame(columns=self.columns)

    def calculate_bmi(self, weight, height):
        """Tính BMI theo công thức"""
        try:
            w, h = float(weight), float(height)
            return round(w / (h ** 2), 2) if h > 0 else 0
        except: return 0

    def get_age_group(self, age):
        """Phân nhóm để phân tích xu hướng sức khỏe"""
        try:
            a = int(age)
            if a < 30: return 'Thanh niên'
            elif a <= 50: return 'Trung niên'
            return 'Người cao tuổi'
        except: return 'N/A'

    def get_processed_data(self):
        temp_df = self.df.copy()
        if not temp_df.empty:
            temp_df['BMI'] = temp_df.apply(lambda x: self.calculate_bmi(x['Cân nặng'], x['Chiều cao']), axis=1)
            temp_df['Nhóm tuổi'] = temp_df['Tuổi'].apply(self.get_age_group)
        return temp_df

    def save(self):
        self.df.to_csv(self.data_path, index=False)