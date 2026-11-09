# Mã nguồn 2.9 - Minh họa hàm băm SHA-256 với các đầu vào khác nhau
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 72
# Trích tự động từ chapters/ch2/main.tex (dòng 2096) bằng extract.py; không sửa tay file này.

import hashlib

# SHA-256: mọi đầu vào → 256 bit (32 byte = 64 hex chars)
inputs = [
    b"Hello",
    b"Hello!",           # Chỉ thêm 1 ký tự
    b"A" * 1000000,      # 1 triệu chữ A
    b"",                 # Chuỗi rỗng
]

for data in inputs:
    h = hashlib.sha256(data).hexdigest()
    preview = data[:16].decode(errors='replace')  # 16 ký tự đầu
    if len(data) > 16:
        preview += "..."                           # đầu vào bị cắt bớt
    label = f'SHA256("{preview}")'
    print(f"{label:<28} = {h[:16]}...")
