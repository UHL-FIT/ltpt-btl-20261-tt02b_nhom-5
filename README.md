# 🩺 Phần Mềm Quản Lý Hồ Sơ Bệnh Nhân (UHL-FIT)

Dự án Bài tập lớn xây dựng ứng dụng máy tính (Desktop Application) hỗ trợ quản lý, theo dõi hồ sơ y tế và phân tích chỉ số sức khỏe y khoa của bệnh nhân dựa trên mô hình kiến trúc phần mềm tiêu chuẩn.

---

## 🏗️ Kiến Trúc Thiết Kế Phần Mềm
Dự án được phân rã chặt chẽ theo mô hình **MVC (Model - View - Controller)** giúp tách biệt hoàn toàn giữa giao diện đồ họa, logic nghiệp vụ toán học và cơ sở dữ liệu:

* **Model (`models/`)**: Phụ trách lưu trữ trạng thái dữ liệu nền tảng, thực thi các thuật toán y khoa động (tính toán BMI theo chuẩn Châu Á IDI&WPRO, phân nhóm tuổi) và ghi/đọc dữ liệu file phẳng CSV bằng thư viện `Pandas`.
* **View (`views/`)**: Phụ trách toàn bộ thành phần đồ họa trực quan sử dụng thư viện `Tkinter` & `TTK`. Tích hợp bố cục thông minh cho phép tự động co giãn (`auto-resize/align`) linh hoạt khi phóng to cửa sổ.
* **Controller (`controllers/`)**: Bộ não điều phối trung tâm. Tiếp nhận mọi sự kiện tương tác thiết bị ngoại vi (Click chuột, Double-click tiêu đề bảng), thực thi quy trình thẩm định dữ liệu đầu vào (`Input Validation`) và bẫy lỗi phòng vệ (`Exception Handling`).

---

## 🛠️ Công Nghệ & Thư Viện Sử Dụng
* **Ngôn ngữ chính**: Python.
* **Giao diện đồ họa (GUI)**: Tkinter & TTK (Themed Tkinter) tích hợp bộ theme hệ thống mở rộng `clam` giúp tùy biến sâu màu sắc.
* **Xử lý dữ liệu & Thống kê**: `Pandas` và `Numpy` (Vectorization tăng tốc xử lý mảng tốc độ cao).
* **Nhật ký vận hành**: Thư viện `Logging` tiêu chuẩn để kiểm soát tiến trình chạy ngầm của hệ thống.

---

## 📁 Cấu Trúc Thư Mục Dự Án
```text
QL_BenhNhan/
│
├── data/
│   ├── patients.csv      # Cơ sở dữ liệu file phẳng lưu trữ thông tin bệnh nhân
│   └── app.log           # File lưu vết lịch sử lỗi và hoạt động của hệ thống
│
├── models/
│   └── patient_model.py  # Định nghĩa cấu trúc bảng DataFrame và thuật toán BMI
│
├── views/
│   └── main_view.py      # Xây dựng layout manager (.pack, .grid) và phong cách widget
│
├── controllers/
│   └── patient_controller.py # Bẫy lỗi, validate dữ liệu đầu vào và bắt sự kiện chuột
│
├── utils/
│   └── logger.py         # Tiện ích ghi log lịch sử đồng thời ra Terminal và File
│
└── main.py               # Điểm mồi (Entry-point) khởi chạy toàn bộ phần mềm
```
## 🛡️ Cơ Chế Xử Lý Ngoại Lệ & Kiểm Thử Phòng Vệ (Exception Handling)
Ứng dụng được thiết kế dựa trên tư duy lập trình phòng vệ, đảm bảo hệ thống hoạt động ổn định trước các hành vi sai lệch của người dùng:

Chặn Dữ Liệu Số Âm / Sai Định Dạng: Mọi trường dữ liệu số (Tuổi, Cân nặng, Chiều cao) đều được Controller lọc qua hàm _validate_positive_number. Nếu người dùng nhập chữ hoặc số ≤0, hệ thống lập tức chặn đứng và cảnh báo trực quan.

Khắc Phục Ô Trống NaN Trong CSV: Khi đọc tệp dữ liệu phẳng, Pandas tự động hiểu ô trống là float (NaN). Controller đã ép kiểu chuỗi chủ động str() trước khi xử lý viết hoa chữ .upper(), triệt tiêu hoàn toàn lỗi sập ứng dụng AttributeError.

Bẫy Lỗi Thao Tác Sai Vị Trí: Nếu người dùng nhấn nút "Xóa bệnh nhân" hoặc "Sửa thông tin" khi chưa chọn bất kỳ dòng nào trên bảng danh sách Treeview, hệ thống sẽ bẫy lỗi bằng mệnh đề điều kiện, đưa ra hộp thoại nhắc nhở thay vì làm treo luồng chương trình.

## 🚀 Hướng Dẫn Cài Đặt & Khởi Chạy
1. Cài đặt các thư viện phụ thuộc
Hệ thống yêu cầu cài đặt thư viện xử lý dữ liệu nâng cao pandas:

pip install pandas
2. Khởi chạy ứng dụng
Di chuyển vào thư mục gốc của dự án và chạy tệp mồi bằng câu lệnh:

python main.py
© Dự án được phát triển và hoàn thiện bởi Nhóm 5 - UHL FIT.
