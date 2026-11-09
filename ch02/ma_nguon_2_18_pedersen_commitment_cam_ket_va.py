# Mã nguồn 2.18 - Pedersen Commitment: cam kết và mở giá trị bí mật
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 86
# Trích tự động từ chapters/ch2/main.tex (dòng 2912) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.17 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_17_lop_ellipticcurve_tim_cap_nhom import *  # noqa
# --- Hết phần thêm ---

# === lab2_commitment.py – Pedersen Commitment ===
# Cam kết giá trị v bằng: C = [v]G + [r]H
# trong đó r là blinding factor ngẫu nhiên.
# Tính chất: hiding (r che giấu v) + binding (không đổi v được).

import random
from math import gcd
random.seed(2026)  # Cố định hạt giống để kết quả tái lập được

# Đường cong nhỏ cho demo
E = EllipticCurve(a=1, b=1, p=23)
G = E.point(0, 1)
order = 28  # Bậc nhóm, G là phần tử sinh (tính từ lab trước)

# H = điểm "ngẫu nhiên" mà không ai biết log_G(H)
# (trong thực tế: H = hash_to_curve("some string"))
k_H = 9                      # Đơn giản hóa – thực tế KHÔNG được biết k_H
assert gcd(k_H, order) == 1  # H cũng sinh toàn bộ nhóm => hiding hoàn hảo
H = k_H * G

def commit(v, r):
    """Pedersen commitment: C = [v]G + [r]H"""
    return v * G + r * H

def verify_opening(C, v, r):
    """Kiểm tra: C == [v]G + [r]H ?"""
    return C == v * G + r * H

# === Demo ===
v_secret = 5    # Giá trị bí mật (ví dụ: tuổi, số dư, ...)
r_blind = random.randrange(order)  # Blinding factor, đều trên {0..order-1}

# Prover cam kết
C = commit(v_secret, r_blind)
print(f"Giá trị bí mật:   v = {v_secret}")
print(f"Blinding factor:  r = {r_blind}")
print(f"Commitment:       C = {C}")

# Verifier chỉ thấy C – không biết v hay r

# Prover mở commitment (reveal)
print(f"\nProver mở: v={v_secret}, r={r_blind}")
print(f"Verify: {verify_opening(C, v_secret, r_blind)}")  # True

# Thử gian lận: mở với v khác, r đoán ngẫu nhiên
# (nhóm chỉ có 28 phần tử nên xác suất đoán trúng là 1/28)
v_fake = 10
r_fake = random.randrange(order)
print(f"\nThử gian lận: v={v_fake}, r={r_fake}")
print(f"Verify: {verify_opening(C, v_fake, r_fake)}")  # False
