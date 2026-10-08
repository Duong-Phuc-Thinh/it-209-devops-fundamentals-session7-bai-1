import os
import sys
import subprocess
import datetime

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Lỗi thực thi lệnh: {' '.join(command)}")
        print(f"Chi tiết lỗi: {e.stderr}")
        sys.exit(1)

def main():
    # Kiểm tra quyền root
    if os.getuid() != 0:
        print("Lỗi: Bạn cần chạy script này với quyền root (sudo python3 setup_sftp.py).")
        sys.exit(1)

    print("=== Bắt đầu cấu hình môi trường SFTP ===")
    username = "sftp-user"
    password = "SftpUserSecurePassword123!"

    # Tạo người dùng sftp-user nếu chưa tồn tại
    try:
        subprocess.run(["id", username], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Người dùng '{username}' đã tồn tại từ trước.")
    except subprocess.CalledProcessError:
        print(f"Đang tạo người dùng '{username}'...")
        run_command(["useradd", "-m", "-s", "/bin/bash", username])
        
        # Thiết lập mật khẩu
        p1 = subprocess.Popen(["echo", f"{username}:{password}"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["chpasswd"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p2.communicate()
        print(f"Đã thiết lập mật khẩu thành công.")

    # Tạo thư mục /var/log/app-backup/
    backup_dir = "/var/log/app-backup"
    print(f"Đang tạo thư mục {backup_dir}...")
    os.makedirs(backup_dir, exist_ok=True)

    # Tạo tệp tin log giả lập
    log_file = os.path.join(backup_dir, "backup-check.log")
    print(f"Đang khởi tạo tệp log giả lập tại: {log_file}...")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"Backup status: SUCCESS at {timestamp}\nDatabase dump completed successfully.\nAll checks passed.\n"
    with open(log_file, "w") as f:
        f.write(log_content)

    # Cấp quyền sở hữu và phân quyền truy cập
    print("Đang thiết lập quyền sở hữu và phân quyền (chmod/chown)...")
    try:
        import grp
        gid_sftp = grp.getgrnam(username).gr_gid
        
        # chown -R root:sftp-user /var/log/app-backup
        os.chown(backup_dir, 0, gid_sftp)
        os.chown(log_file, 0, gid_sftp)
        
        # chmod 750 /var/log/app-backup
        os.chmod(backup_dir, 0o750)
        
        # chmod 640 /var/log/app-backup/backup-check.log
        os.chmod(log_file, 0o640)
        
        print("Thiết lập quyền thành công!")
    except Exception as e:
        print(f"Lỗi khi phân quyền: {e}")
        sys.exit(1)

    print("\n=== KIỂM TRA THÔNG TIN HỆ THỐNG ===")
    print("Thông tin người dùng:")
    print(run_command(["id", username]))
    print("\nThông tin tệp tin log:")
    print(run_command(["ls", "-l", log_file]))
    
    print("\n=== THÔNG TIN KẾT NỐI SFTP CHO CLIENT (WINDOWS) ===")
    print(f"- Host: <IP_CỦA_VPS>")
    print(f"- Port: 22")
    print(f"- Username: {username}")
    print(f"- Password: {password}")
    print(f"- Remote Path: {log_file}")
    print("====================================================")

if __name__ == "__main__":
    main()