# Mã nguồn 5.6 - Lab 5.2: Miền H, L và nội suy trace thành đa thức bằng Lagrange
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 247
# Trích tự động từ chapters/ch5/main.tex (dòng 3109) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.5 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_05_lab_5_1_tao_execution import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 2: Miền H, L và nội suy trace -> đa thức t(x)
# ============================================================
g = 5                                   # phần tử sinh của F_97^*
n, blowup = len(trace), 4               # 4 hàng, rho = 1/4
N = n * blowup                          # |L| = 16
kappa = pow(g, (p - 1) // N, p)         # 8: sinh nhóm con cấp 16
omega = pow(kappa, blowup, p)           # 22: sinh nhóm con cấp 4
H = [pow(omega, i, p) for i in range(n)]              # miền trace
L = [g * pow(kappa, j, p) % p for j in range(N)]      # coset g * <kappa>

def lagrange_eval(values, dom, x_eval):
    """Nội suy Lagrange: f(x_eval) từ các cặp (dom[i], values[i])."""
    result = 0
    for i in range(len(values)):
        num, den = 1, 1
        for j in range(len(values)):
            if i != j:
                num = mod(num * (x_eval - dom[j]))
                den = mod(den * (dom[i] - dom[j]))
        result = mod(result + values[i] * num * inv(den))
    return result

print("\n=== Miền và nội suy ===")
print(f"  H = {H}")
print(f"  L = {L}")
print(f"  L giao H = {set(L) & set(H)}")                    # phải rỗng
print(f"  t(H) = {[lagrange_eval(trace, H, x) for x in H]}")  # phải bằng trace
tL = [lagrange_eval(trace, H, x) for x in L]          # low-degree extension
print(f"  t|L  = {tL}")
# Cấu trúc của L: omega * L[j] = L[j+4], -L[j] = L[j+8]
print(f"  omega*L[j] = L[j+4]: {all(omega * L[j] % p == L[(j + 4) % N] for j in range(N))}")
print(f"  -L[j] = L[j+8]:      {all((-L[j]) % p == L[(j + 8) % N] for j in range(N))}")
