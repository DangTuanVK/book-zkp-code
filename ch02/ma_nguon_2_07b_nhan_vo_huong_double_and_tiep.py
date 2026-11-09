# Mã nguồn 2.7b - (phần nối tiếp của Mã nguồn 2.7)
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 59
# Trích tự động từ chapters/ch2/main.tex (dòng 1231) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.7 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_07_nhan_vo_huong_double_and import *  # noqa
# --- Hết phần thêm ---

# --- ECDLP: tính ngược rất khó ---
# Cho Q = [k]G, tìm k?
k_secret = 17
Q = scalar_mult(k_secret, G, a, p)
print(f"\nBí mật k = {k_secret}")
print(f"Public Q = [k]G = {Q}")
print(f"Với p = 23, brute force dễ dàng.")
print(f"Với p ~ 2^256, cần ~2^128 phép tính – KHÔNG KHẢ THI!")
