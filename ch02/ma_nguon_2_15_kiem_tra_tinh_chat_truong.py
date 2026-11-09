# Mã nguồn 2.15 - Kiểm tra tính chất trường F_17
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 81
# Trích tự động từ chapters/ch2/main.tex (dòng 2722) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.14 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_14_lop_fp_hoan_chinh_truong import *  # noqa
# --- Hết phần thêm ---

# === Kiểm tra tính chất trường F_17 ===
p = 17
a, b, c = Fp(7, p), Fp(11, p), Fp(5, p)
assert (a+b)+c == a+(b+c), "Kết hợp cộng sai"
assert a*b == b*a, "Giao hoán nhân sai"
assert a*(b+c) == a*b + a*c, "Phân phối sai"
assert a * a.inv() == 1, "Nghịch đảo sai"
assert a**(p-1) == 1, "Fermat nhỏ sai"
print(f"Tất cả tính chất trường F_{p} đúng!")
print(f"  a+b={a+b}, a*b={a*b}, a/b={a/b}, a^(-1)={a.inv()}")
