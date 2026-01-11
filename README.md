# 💼 Hệ Thống Quản Lý Thiết Bị CNTT Doanh Nghiệp

> **Business IT Device Management System** – Ứng dụng quản lý thiết bị CNTT toàn diện cho doanh nghiệp, được xây dựng bằng **Python & PyQt6**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-Educational-orange)

---

## 📌 Giới Thiệu

**Hệ Thống Quản Lý Thiết Bị CNTT** là một ứng dụng desktop hỗ trợ doanh nghiệp quản lý toàn bộ vòng đời của thiết bị CNTT:

* Từ **mua sắm – sử dụng – bảo trì – thanh lý**
* Phân quyền rõ ràng theo **vai trò người dùng**
* Giao diện trực quan, dễ sử dụng

Phù hợp cho:

* Doanh nghiệp vừa và nhỏ
* Môi trường học tập, đồ án môn học
* Dự án demo về **OOP, UML, PyQt6, SQLite**

---

## ✨ Tính Năng Chính

### 👤 Quản Lý Người Dùng

* Phân quyền theo vai trò: **Admin / Nhân viên / Kỹ thuật viên**
* Đăng nhập & xác thực người dùng
* Quản lý nhân viên và phòng ban
* Quản lý tài khoản và mật khẩu

### 💻 Quản Lý Thiết Bị

* Thêm, cập nhật, thanh lý thiết bị CNTT
* Quản lý thông tin chi tiết (model, serial, loại thiết bị, trạng thái)
* Kho thiết bị với **tìm kiếm & lọc nâng cao**
* Theo dõi trạng thái:

  * Sẵn sàng
  * Đang sử dụng
  * Đang bảo trì
  * Đã thanh lý

### 📋 Quản Lý Phân Công

* Phân công thiết bị cho nhân viên
* Thu hồi & phân công lại thiết bị
* Theo dõi thiết bị theo **nhân viên / phòng ban**
* Lưu lịch sử phân công & kiểm toán

### 🔧 Quản Lý Bảo Trì

* Báo cáo sự cố thiết bị
* Tạo & theo dõi phiếu bảo trì
* Quy trình xử lý:

  * Chờ xử lý → Đang xử lý → Hoàn thành
* Phân công kỹ thuật viên
* Lưu lịch sử bảo trì

### 📊 Dashboard & Báo Cáo

* Tổng quan hệ thống theo thời gian thực
* Thống kê số lượng & trạng thái thiết bị
* Phân tích thiết bị theo phòng ban
* Xuất dữ liệu & báo cáo

---

## 🧑‍💼 Vai Trò & Quyền Hạn

### 🔑 Quản Trị Viên (Admin)

* Toàn quyền truy cập hệ thống
* Quản lý thiết bị, nhân viên, phòng ban
* Phân công & thu hồi thiết bị
* Xem và xuất báo cáo
* Duyệt yêu cầu thiết bị

### 👨‍💻 Nhân Viên

* Yêu cầu cấp thiết bị
* Xem thiết bị được phân công
* Báo cáo sự cố
* Xem lịch sử sử dụng thiết bị

### 🛠️ Kỹ Thuật Viên

* Xem danh sách phiếu bảo trì
* Xử lý & cập nhật trạng thái bảo trì
* Hoàn thành & đóng phiếu bảo trì

---

## ⚙️ Yêu Cầu Hệ Thống

* **Python:** 3.8 trở lên
* **pip:** Trình quản lý gói Python

---

## 🚀 Cài Đặt

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Bonkaaa/Business_device_management_system.git
cd Business_device_management_system
```

### 2️⃣ Cài Đặt Thư Viện

```bash
pip install -r requirement.txt
```

---

## ▶️ Sử Dụng

### 🔹 Chạy Từ Mã Nguồn

```bash
python src/main.py
```

Hoặc:

```bash
python -m src.main
```

### 🔹 Biên Dịch File Thực Thi

**Windows (CMD):**

```batch
.\scripts\build.bat
```

**Windows (PowerShell):**

```powershell
.\scripts\build.ps1
```

**Linux / macOS / Git Bash:**

```bash
chmod +x ./scripts/install_app.sh
./scripts/install_app.sh
```

📦 File thực thi sẽ nằm trong thư mục **`dist/`**

---

## 🔐 Tài Khoản Mặc Định

| Username | Password | Role          |
| -------- | -------- | ------------- |
| admin    | admin123 | Quản trị viên |

⚠️ **Khuyến nghị:** Đổi mật khẩu ngay sau lần đăng nhập đầu tiên.

---

## 🗂️ Cấu Trúc Dự Án

```
Business_device_management_system/
├── src/
│   ├── base/            # Lớp cơ sở & abstraction
│   ├── database/        # Kết nối & thao tác SQLite
│   ├── entities/        # Các mô hình dữ liệu
│   ├── manager/         # Xử lý logic nghiệp vụ
│   ├── ui/              # Giao diện PyQt6
│   ├── utils/           # Hàm tiện ích & hằng số
│   └── main.py          # Entry point
├── scripts/             # Script build & cài đặt
├── image/               # Ảnh chụp & sơ đồ
├── uml_diagram/         # UML source
├── requirement.txt
└── README.md
```

---

## 🧩 UML & Tài Liệu Thiết Kế

* 📌 **Use Case Diagram:** `image/usecase.png`
* 📌 **Class Diagram:** `image/class_diagram.png`
* 📌 **Sequence Diagram:**

  * Phân công thiết bị
  * Bảo trì thiết bị
  * Thu hồi thiết bị

---

## 🗄️ Cơ Sở Dữ Liệu

* **Hệ quản trị:** SQLite3
* **File:** `data/sharedatabase.db`

📍 Tự động tạo khi chạy ứng dụng lần đầu

---

## 🛠️ Phát Triển & Mở Rộng

Cách thêm tính năng mới:

1. Thêm entity trong `src/entities/`
2. Viết logic trong `src/manager/`
3. Tạo UI trong `src/ui/`
4. Cập nhật database nếu cần
5. Kiểm thử với nhiều vai trò người dùng

---

## 🐞 Xử Lý Sự Cố

### ❌ Ứng dụng không chạy

* Kiểm tra Python >= 3.8
* Cài đủ thư viện: `pip install -r requirement.txt`

### ❌ Lỗi Database

* Xóa thư mục `data/` để reset CSDL

### ❌ Build thất bại

* Cài PyInstaller: `pip install pyinstaller`
* Kiểm tra log lỗi trong terminal

---

## 📄 Giấy Phép

Dự án phục vụ **mục đích học tập & cá nhân**.

---

## 🤝 Đóng Góp

* Issues & Pull Requests luôn được hoan nghênh 💙

---

## 📬 Liên Hệ

Nếu có câu hỏi hoặc cần hỗ trợ, vui lòng tạo **Issue** trên GitHub repository.

---

✨ *Cảm ơn bạn đã sử dụng Hệ Thống Quản Lý Thiết Bị CNTT!*
