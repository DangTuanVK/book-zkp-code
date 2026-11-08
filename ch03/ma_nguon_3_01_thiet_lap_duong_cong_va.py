# Mã nguồn 3.1 - Thiết lập đường cong và sinh cặp khóa cho Schnorr ZKP
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 3, trang 98
# Trích tự động từ chapters/ch3/main.tex (dòng 760) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.17 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_17_lop_ellipticcurve_tim_bac_nhom import *  # noqa
# --- Hết phần thêm ---

# === lab3_schnorr.py – Schnorr ZKP hoàn chỉnh ===

import hashlib
import random

# --- Tái sử dụng class Fp và ECPoint từ chương 2 ---
# (giả sử đã import hoặc copy ở trên)

# ============================================================
# SETUP: Đường cong E(F_23): y^2 = x^3 + x + 1
# (nhỏ để dễ quan sát – production dùng BN254/BLS12-381)
# ============================================================
p = 23
E = EllipticCurve(a=1, b=1, p=p)
G = E.point(0, 1)

# Tìm bậc nhóm (order)
order = None
Q = G
for k in range(1, 100):
    Q = Q + G if k > 1 else G
    kG = (k + 1) * G  # Đơn giản: dùng scalar_mult
# Cách nhanh hơn:
order = 28  # Đã tính ở lab chương 2

print(f"Đường cong: y^2 = x^3 + x + 1 (mod {p})")
print(f"Generator G = {G}, order = {order}")

# ============================================================
# KEY GENERATION
# ============================================================
x_secret = random.randint(1, order - 1)  # Witness (bí mật)
H_public = x_secret * G                  # Statement (công khai)
print(f"\n--- Key Generation ---")
print(f"Secret key x = {x_secret}")
print(f"Public key H = [x]G = {H_public}")
