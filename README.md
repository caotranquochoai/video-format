# 🔐 Video Folder Encryptor (.vcc)

Một công cụ Python mã nguồn mở để **mã hóa toàn bộ thư mục chứa video**, bao gồm cả video trong thư mục con. Đặc biệt, **tên file gốc sẽ được mã hóa và ẩn**, chỉ được khôi phục khi giải mã bằng đúng mật khẩu.

## ✨ Tính năng nổi bật

- ✅ Mã hóa toàn bộ thư mục và thư mục con
- ✅ Ẩn hoàn toàn tên video gốc khi mã hóa
- ✅ Giải mã và khôi phục đúng tên file gốc
- ✅ Dùng AES-256 (CBC) để mã hóa nội dung
- ✅ Dùng AES (ECB) để mã hóa tên file
- ✅ Dễ sử dụng qua giao diện dòng lệnh (CLI)

## 🛠 Yêu cầu hệ thống

- Python 3.6+
- PyCryptodome

Cài đặt:

```bash
pip install pycryptodome
```

## 🚀 Cách sử dụng

### 1. Mã hóa thư mục:

```bash
python video_protect_folder_cli_vcc_secure_name.py encrypt ./MyVideos ./EncryptedVideos
🔑 Nhập mật khẩu:
```

### 2. Giải mã thư mục:

```bash
python video_protect_folder_cli_vcc_secure_name.py decrypt ./EncryptedVideos ./RestoredVideos
🔑 Nhập mật khẩu:
```

## 📦 Cấu trúc file `.vcc`

- 16 byte đầu: IV (AES CBC)
- 2 byte tiếp theo: Độ dài tên file đã mã hóa
- Tiếp theo: Tên file gốc đã được AES mã hóa
- Phần còn lại: Dữ liệu video đã được AES CBC mã hóa

## ⚠️ Cảnh báo bảo mật

- Nếu mất mật khẩu, **không thể giải mã** hoặc khôi phục tên file gốc.
- Đảm bảo bạn **sao lưu đúng mật khẩu** ở nơi an toàn.

## 📝 Giấy phép

MIT License

## 👨‍💻 Tác giả

**VivuCloud**
