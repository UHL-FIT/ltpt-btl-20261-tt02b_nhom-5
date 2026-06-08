import logging # Thư viện nhật ký tiêu chuẩn của Python, dùng thay thế lệnh print để quản lý tiến trình khoa học hơn
import os      # Thư viện quản lý tệp tin hệ thống

def setup_logger(name, log_file="data/app.log", level=logging.INFO):
    """Hàm khởi tạo bộ ghi nhật ký (Logger): Tự động xuất lịch sử phần mềm ra màn hình Terminal và lưu vào file app.log"""
    
    # Đảm bảo thư mục 'data/' lưu trữ file nhật ký được tạo ra an toàn, tránh lỗi Crash phần mềm do thiếu thư mục
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Định nghĩa cấu trúc một dòng log tiêu chuẩn: [Thời gian chạy] [Tên tầng chức năng] [Mức độ lỗi] - Nội dung thông điệp cụ thể
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 1. BỘ GHI FILE (FileHandler): Chịu trách nhiệm ghi đè/nối tiếp lịch sử chạy lâu dài xuống tệp tin data/app.log trên ổ cứng
    file_handler = logging.FileHandler(log_file, encoding='utf-8') # Ép bảng mã UTF-8 để lưu tiếng Việt không lỗi font
    file_handler.setFormatter(formatter) # Áp dụng định dạng dòng log

    # 2. BỘ XUẤT MÀN HÌNH (StreamHandler): Bắn trực tiếp các thông tin ghi nhận ra màn hình Command Prompt/Terminal khi lập trình viên đang chạy thử
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Khởi tạo hoặc tái sử dụng một kênh Logger dựa trên tên định danh truyền vào (Ví dụ: 'patient_model', 'patient_controller')
    logger = logging.getLogger(name)
    logger.setLevel(level) # Đặt ngưỡng lọc thông tin nhật ký (mặc định chỉ ghi nhận mức INFO, WARNING, ERROR, CRITICAL)

    # Kiểm tra phòng vệ: Nếu kênh logger này chưa được đấu nối với bộ ghi nào thì mới tiến hành thêm vào, tránh việc log bị lặp chữ nhiều lần
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger # Trả về thực thể bộ ghi hoàn chỉnh để các file Model, Controller nhúng vào sử dụng
