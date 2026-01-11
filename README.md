# Hệ Thống Quản Lý Thiết Bị Doanh Nghiệp

Một hệ thống quản lý thiết bị CNTT toàn diện được xây dựng bằng PyQt6 để quản lý tài sản phần cứng doanh nghiệp, phân công thiết bị cho nhân viên và các yêu cầu bảo trì.

## Tổng Quan

Ứng dụng này cung cấp giải pháp hoàn chỉnh cho việc quản lý thiết bị CNTT trong môi trường doanh nghiệp. Hệ thống hỗ trợ nhiều vai trò người dùng (Quản trị viên, Nhân viên, Kỹ thuật viên) và xử lý toàn bộ chu trình vòng đời của thiết bị từ khâu mua sắm đến thanh lý, bao gồm theo dõi phân công và quản lý bảo trì.

## Tính Năng

### 👤 Quản Lý Người Dùng
- **Kiểm soát truy cập theo vai trò** (Quản trị viên, Nhân viên, Kỹ thuật viên)
- Hệ thống đăng nhập bảo mật với quản lý mật khẩu
- Quản lý phòng ban và nhân viên
- Đăng ký và xác thực người dùng

### 💻 Quản Lý Thiết Bị
- Thêm, cập nhật và thanh lý thiết bị CNTT
- Theo dõi thông tin chi tiết thiết bị (model, số serial, trạng thái, v.v.)
- Kho thiết bị với khả năng tìm kiếm và lọc
- Theo dõi trạng thái thiết bị (Sẵn sàng, Đang sử dụng, Đang bảo trì, Đã thanh lý)

### 📋 Quản Lý Phân Công
- Phân công thiết bị cho nhân viên
- Theo dõi phân công thiết bị theo nhân viên và phòng ban
- Thu hồi và phân công lại thiết bị
- Lịch sử phân công và kiểm toán

### 🔧 Quản Lý Bảo Trì
- Báo cáo sự cố thiết bị
- Tạo và theo dõi yêu cầu bảo trì
- Quy trình bảo trì (Đang chờ, Đang xử lý, Hoàn thành)
- Phân công kỹ thuật viên cho các tác vụ bảo trì
- Lịch sử và trạng thái bảo trì

### 📊 Bảng Điều Khiển & Báo Cáo
- Thống kê và tổng quan theo thời gian thực
- Số liệu về tính khả dụng của thiết bị
- Phân phối thiết bị theo phòng ban
- Xuất báo cáo và dữ liệu

## Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- pip (công cụ cài đặt gói Python)

## Cài Đặt

1. **Clone repository**
   ```bash
   git clone https://github.com/Bonkaaa/Business_device_management_system.git
   cd Business_device_management_system
   ```

2. **Cài đặt các gói cần thiết**
   ```bash
   pip install -r requirement.txt
   ```

## Sử Dụng

### Chạy Từ Mã Nguồn

Di chuyển đến thư mục `src` và chạy:

```bash
python src/main.py
```

Hoặc từ thư mục gốc của dự án:

```bash
python -m src.main
```

### Biên Dịch File Thực Thi

Dự án bao gồm các script biên dịch cho nhiều nền tảng khác nhau:

#### Windows (Command Prompt)
```batch
.\scripts\build.bat
```

#### Windows (PowerShell)
```powershell
.\scripts\build.ps1
```

#### Linux/Mac/Git Bash
```bash
chmod +x ./scripts/install_app.sh
./scripts/install_app.sh
```

File thực thi sẽ được tạo trong thư mục `dist`.

## Tài Khoản Mặc Định

Hệ thống tạo tài khoản mặc định khi chạy lần đầu:

| Tên đăng nhập | Mật khẩu | Vai trò        |
|---------------|----------|----------------|
| admin         | admin123 | Quản trị viên  |

**⚠️ Quan trọng:** Hãy đổi mật khẩu mặc định sau khi đăng nhập lần đầu!

## Vai Trò Người Dùng & Quyền Hạn

### Quản Trị Viên
- Toàn quyền truy cập hệ thống
- Quản lý thiết bị (thêm, cập nhật, thanh lý)
- Quản lý nhân viên và phòng ban
- Phân công/thu hồi thiết bị
- Xem tất cả báo cáo và thống kê
- Duyệt/từ chối yêu cầu thiết bị

### Nhân Viên
- Yêu cầu thiết bị
- Xem thiết bị được phân công
- Báo cáo sự cố thiết bị
- Xem lịch sử thiết bị cá nhân

### Kỹ Thuật Viên
- Xem yêu cầu bảo trì
- Xử lý và hoàn thành các tác vụ bảo trì
- Cập nhật trạng thái bảo trì
- Đóng phiếu bảo trì

## Công Nghệ Sử Dụng

- **Giao diện:** PyQt6 (framework GUI)
- **Cơ sở dữ liệu:** SQLite3 (cơ sở dữ liệu nhúng)
- **Định dạng dữ liệu:** JSON (để import/export dữ liệu)
- **Công cụ biên dịch:** PyInstaller (tạo file thực thi độc lập)
- **Ngôn ngữ:** Python 3.8+

## Cấu Trúc Dự Án

```
Business_device_management_system/
├── src/
│   ├── base/           # Các lớp cơ sở và abstraction
│   ├── database/       # Kết nối và thao tác cơ sở dữ liệu
│   ├── entities/       # Mô hình dữ liệu (Device, Employee, Department, v.v.)
│   ├── manager/        # Các manager xử lý logic nghiệp vụ
│   │   ├── auth_manager.py
│   │   ├── inventory.py
│   │   ├── hr_manager.py
│   │   ├── assignment_manager.py
│   │   └── maintenance_manager.py
│   ├── ui/             # Các thành phần giao diện PyQt6
│   │   ├── main_window.py
│   │   ├── login_window.py
│   │   ├── inventory_tab.py
│   │   ├── hr_tab.py
│   │   ├── assignment_tab.py
│   │   └── maintenance_tab.py
│   ├── utils/          # Các hàm tiện ích và hằng số
│   └── main.py         # Điểm khởi đầu ứng dụng
├── scripts/            # Script biên dịch và cài đặt
├── image/              # Ảnh chụp màn hình và sơ đồ ứng dụng
├── uml_diagram/        # File mã nguồn sơ đồ UML
├── requirement.txt     # Các thư viện Python cần thiết
└── README.md           # File này
```

## Sơ Đồ UML

Dự án bao gồm các sơ đồ UML chi tiết trong thư mục `image/` và `uml_diagram/`:

- **Sơ đồ Use Case** (`image/usecase.png`) - Tổng quan chức năng hệ thống
- **Sơ đồ Class** (`image/class_diagram.png`) - Kiến trúc hệ thống
- **Sơ đồ Sequence:**
  - Quy trình phân công (`image/assignment_sq_diagram.png`)
  - Quy trình bảo trì (`image/maintanance_sq_diagram.png`)
  - Quy trình thu hồi thiết bị (`image/return_device_sq_diagram.png`)

## Cơ Sở Dữ Liệu

Ứng dụng sử dụng SQLite3 để lưu trữ dữ liệu. File cơ sở dữ liệu (`sharedatabase.db`) được tự động tạo trong thư mục `data/` khi chạy lần đầu.

### Vị Trí Cơ Sở Dữ Liệu

- **Chạy từ mã nguồn:** `data/sharedatabase.db` (trong thư mục gốc dự án)
- **Chạy từ file thực thi:** `data/sharedatabase.db` (bên cạnh file .exe)

## Phát Triển

### Cấu Trúc Code

Ứng dụng tuân theo kiến trúc module:

- **Entities:** Các mô hình dữ liệu đại diện cho đối tượng nghiệp vụ
- **Managers:** Lớp logic nghiệp vụ xử lý các thao tác
- **UI:** Lớp hiển thị với các thành phần PyQt6
- **Database:** Lớp truy cập dữ liệu cho thao tác SQLite
- **Utils:** Các hàm hỗ trợ và hằng số

### Thêm Tính Năng Mới

1. Định nghĩa entities trong `src/entities/`
2. Triển khai logic nghiệp vụ trong manager phù hợp (`src/manager/`)
3. Tạo các thành phần UI trong `src/ui/`
4. Cập nhật schema cơ sở dữ liệu nếu cần
5. Test với các vai trò người dùng khác nhau

## Xử Lý Sự Cố

### Ứng dụng không khởi động
- Đảm bảo Python 3.8+ đã được cài đặt
- Xác minh tất cả các thư viện đã được cài đặt: `pip install -r requirement.txt`
- Kiểm tra thông báo lỗi trong console

### Lỗi cơ sở dữ liệu
- Xóa thư mục `data/` để reset cơ sở dữ liệu
- Các tài khoản mặc định sẽ được tạo lại khi khởi động lần tiếp theo

### Biên dịch thất bại
- Đảm bảo PyInstaller đã được cài đặt: `pip install pyinstaller`
- Kiểm tra các đường dẫn trong script biên dịch là chính xác
- Xem lại output console để biết lỗi cụ thể

## Giấy Phép

Dự án này có sẵn cho mục đích giáo dục và sử dụng cá nhân.

## Đóng Góp

Chúng tôi hoan nghênh các đóng góp! Vui lòng thoải mái gửi issues và pull requests.

## Liên Hệ

Nếu có câu hỏi hoặc cần hỗ trợ, vui lòng mở một issue trên repository GitHub.
