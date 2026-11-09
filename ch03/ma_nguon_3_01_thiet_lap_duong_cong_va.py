# Mã nguồn 3.1 - Thiết lập đường cong và sinh cặp khóa cho Schnorr ZKP
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 3, trang 103
# Trích tự động từ chapters/ch3/main.tex (dòng 870) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.17 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_17_lop_ellipticcurve_tim_cap_nhom import *  # noqa
# --- Hết phần thêm ---

# === lab3_schnorr.py – Schnorr ZKP hoàn chỉnh ===

import hashlib
import random

# --- Tái sử dụng class Fp và ECPoint từ chương 2 ---
# (giả sử đã import hoặc copy ở trên)

random.seed(2024)  # Cố định hạt giống để kết quả tái lập được

# ============================================================
# SETUP: Đường cong E(F_23): y^2 = x^3 + x + 4
# Nhóm điểm có 29 phần tử (số nguyên tố), nên mọi điểm khác O
# đều là phần tử sinh và Z_29 là một trường: (e1 - e2)^(-1) luôn
# tồn tại khi e1 != e2, extractor luôn hoạt động.
# (nhỏ để dễ quan sát – production dùng BN254/BLS12-381)
# ============================================================
p = 23
E = EllipticCurve(a=1, b=4, p=p)
G = E.point(0, 2)

# Tìm bậc của G: số k nhỏ nhất sao cho [k]G = O
order = 1
Q = G
while not Q.is_infinity:
    Q = Q + G
    order += 1

print(f"Đường cong: y^2 = x^3 + x + 4 (mod {p})")
print(f"Generator G = {G}, order = {order} (số nguyên tố)")

# ============================================================
# KEY GENERATION
# ============================================================
x_secret = random.randint(1, order - 1)  # Witness (bí mật)
H_public = x_secret * G                  # Statement (công khai)
print(f"\n--- Key Generation ---")
print(f"Secret key x = {x_secret}")
print(f"Public key H = [x]G = {H_public}")
