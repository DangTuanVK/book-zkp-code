# Mã nguồn 4.7 - Ba tấn công lên một ``SNARK'' chỉ gồm QAP: chọn H sau tau, tự chế C', và dò witness khi không làm mù
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 147
# Trích tự động từ chapters/ch4/main.tex (dòng 2379) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.6 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_06_chuyen_doi_r1cs_sang_qap import *  # noqa
# --- Hết phần thêm ---

# === Ba cách phá một "SNARK" chỉ có QAP (dùng lại hàm ở mã nguồn trước) ===
import random
s_bad = [1, 35, 4, 16, 64 % p]                    # x = 4: KHÔNG thỏa R1CS
Ax, Bx, Cx, P = qap_polys(s_bad)

# --- Tấn công 1: chọn H SAU khi biết tau ---
tau = random.randrange(4, p)                      # tau ngoài {1, 2, 3}
H_tau = poly_eval(P, tau) * pow(poly_eval(Z, tau), p - 2, p) % p
print("[1] H chọn sau tau:  qua kiểm tra =",
      poly_eval(P, tau) == H_tau * poly_eval(Z, tau) % p)

# Nếu H phải cố định TRƯỚC (lấy thương tốt nhất), tau ngẫu nhiên bắt được:
H, _ = poly_divmod(P, Z)
lot = [t for t in range(4, p)
       if poly_eval(P, t) == poly_eval(H, t) * poly_eval(Z, t) % p]
print(f"    H cố định trước: lọt ở {len(lot)}/{p - 4} giá trị tau {lot}")

# --- Tấn công 2: không dùng CÙNG s cho A, B, C ---
_, C_fake = poly_divmod(poly_mul(Ax, Bx), Z)      # C' = A*B mod Z_H
P_fake = poly_add(poly_mul(Ax, Bx), poly_scale(C_fake, -1))
_, rem = poly_divmod(P_fake, Z)
print("[2] C' tự chế:       Z_H | A*B - C' =", rem == [0],
      "| C' = sum s_j c_j ?", C_fake == Cx[:len(C_fake)])

# --- Tấn công 3: rò rỉ witness khi A(tau), B(tau) không được làm mù ---
def AB(x):                    # ai có CRS cũng tính được cặp này cho x thử
    Ax, Bx, *_ = qap_polys([1, 35, x, x * x % p, x**3 % p])
    return poly_eval(Ax, tau), poly_eval(Bx, tau)
seen = AB(3)                                      # Verifier nhìn thấy
print("[3] Không làm mù:    x khớp =", [x for x in range(p) if AB(x) == seen])

delta = random.randrange(1, p)
r_rand, s_rand = random.randrange(p), random.randrange(p)
blind = ((seen[0] + r_rand * delta) % p, (seen[1] + s_rand * delta) % p)
inv = pow(delta, p - 2, p)
# Với MỌI x thử đều có (r', s') giải thích được giá trị đã làm mù:
expl = [((blind[0] - AB(x)[0]) * inv % p, (blind[1] - AB(x)[1]) * inv % p)
        for x in range(p)]
print(f"    Có làm mù:       {len(expl)}/{p} giá trị x đều khả dĩ")
