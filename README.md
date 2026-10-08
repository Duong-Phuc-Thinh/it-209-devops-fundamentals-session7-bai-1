# Quản lý người dùng giới hạn và Truyền tải dữ liệu qua SFTP trên Windows

Thư mục này chứa mã nguồn tự động hóa việc thiết lập người dùng giới hạn `sftp-user`, tạo thư mục log giả lập, cấu hình phân quyền bảo mật trên Linux Server (VPS), và hướng dẫn tải file log về Windows.

## Chức năng của mã nguồn

File `setup_sftp.py` được viết bằng Python giúp tự động thực hiện các thao tác quản trị viên sau trên VPS Linux:
1. Kiểm tra quyền thực thi (`root`).
2. Tạo người dùng mới `sftp-user` kèm thiết lập mật khẩu bảo mật mặc định.
3. Tạo cấu trúc thư mục `/var/log/app-backup/` và ghi đè/tạo mới file `backup-check.log` có chứa thông tin thời gian hiện tại.
4. Gán quyền sở hữu thư mục và tệp tin cho nhóm `sftp-user` đọc, đồng thời ngăn chặn các người dùng thông thường khác truy cập trái phép (`chmod 750` cho thư mục, `640` cho tệp tin log).

## Hướng dẫn sử dụng

### Bước 1: Chạy Script Cấu hình trên VPS Linux

1. Di chuyển file `setup_sftp.py` lên máy chủ VPS Linux của bạn.
2. Thực thi script bằng quyền `sudo`:
   ```bash
   sudo python3 setup_sftp.py
   ```
3. Script sẽ hiển thị kết quả kiểm tra dạng:
   - Thông tin người dùng (`id sftp-user`).
   - Phân quyền tệp tin (`ls -l /var/log/app-backup/backup-check.log`).
   - Thông tin kết nối SFTP.

### Bước 2: Kết nối từ máy tính Windows cá nhân

1. Tải và cài đặt phần mềm SFTP Client như **WinSCP**, **Bitvise SSH Client** hoặc **FileZilla** trên Windows.
2. Khởi chạy phần mềm và nhập các thông tin kết nối:
   - **Host / File protocol**: SFTP
   - **Host Name / IP**: Nhập IP máy chủ VPS của bạn.
   - **Port**: `22`
   - **Username**: `sftp-user`
   - **Password**: `SftpUserSecurePassword123!` (đã được tạo tự động bởi script)
3. Nhấn **Login / Connect** để kết nối.

### Bước 3: Tải file về máy cá nhân

1. Trên cửa sổ quản lý thư mục từ xa (Remote site / Khung bên phải), tìm đường dẫn: `/var/log/app-backup/`.
2. Bạn sẽ thấy tệp tin `backup-check.log` xuất hiện.
3. Thực hiện kéo thả tệp tin này về thư mục cục bộ của máy tính Windows (Khung bên trái).
4. Mở file log đã tải bằng Notepad/VS Code trên Windows để đối chiếu nội dung trùng khớp với trên máy chủ Linux.

### Kết quả mong đợi
- Tài khoản `sftp-user` không có quyền thực thi lệnh `sudo`.
- Tệp tin được tải về an toàn, nguyên vẹn dữ liệu thông qua giao thức SFTP.