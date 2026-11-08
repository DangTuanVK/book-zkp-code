# Mã nguồn 2.7 - Nhân vô hướng double-and-add và tìm bậc nhóm E(F_23)
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 57
# Trích tự động từ chapters/ch2/main.tex (dòng 1158) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.6 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_06_phep_cong_diem_tren_duong import *  # noqa
# --- Hết phần thêm ---

# === Nhân vô hướng và demo ===
def scalar_mult(k, P, a, p):
    """Tính [k]P bằng double-and-add."""
    result = None  # O (phần tử đơn vị)
    current = P
    while k > 0:
        if k & 1:
            result = point_add(result, current, a, p)
        current = point_add(current, current, a, p)  # double
        k >>= 1
    return result

# --- Ví dụ: E(F_23): y^2 = x^3 + x + 1 ---
p, a, b = 23, 1, 1
G = (0, 1)
print("Các bội của G = (0, 1) trên E(F_23):")
for k in range(1, 30):
    kG = scalar_mult(k, G, a, p)
    if kG is None:
        print(f"  [{k}]G = O – bậc nhóm = {k}")
        break
    print(f"  [{k}]G = {kG}")
