# Mã nguồn 4.11 - Nội suy Lagrange chuyển R1CS sang QAP, tính thương h(x) và mô phỏng setup
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 186
# Trích tự động từ chapters/ch4/main.tex (dòng 4028) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.10 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_10_pipeline_r1cs_va_witness_cho import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 3: R1CS → QAP (nội suy Lagrange trên ĐA THỨC)
# ============================================================
# Miền nội suy H = {r_1, r_2, r_3} = {1, 2, 3}
eval_domain = [1, 2, 3]

# --- Đa thức: danh sách hệ số từ bậc thấp đến bậc cao ---
def poly_add(f, g):
    k = max(len(f), len(g))
    f, g = f + [0] * (k - len(f)), g + [0] * (k - len(g))
    return [mod(u + v) for u, v in zip(f, g)]

def poly_scale(f, c): return [mod(c * u) for u in f]

def poly_mul(f, g):
    res = [0] * (len(f) + len(g) - 1)
    for i, u in enumerate(f):
        for j, v in enumerate(g):
            res[i + j] = mod(res[i + j] + u * v)
    return res

def poly_eval(f, x):
    return mod(sum(u * pow(x, i, p) for i, u in enumerate(f)))

def poly_divmod(f, g):
    """Chia f cho g, trả về (thương, dư)."""
    f, q = f[:], [0] * max(len(f) - len(g) + 1, 1)
    for i in range(len(f) - len(g), -1, -1):
        q[i] = mod(f[i + len(g) - 1] * inv(g[-1]))
        for j, v in enumerate(g):
            f[i + j] = mod(f[i + j] - q[i] * v)
    rem = f[:len(g) - 1]
    while len(rem) > 1 and rem[-1] == 0:      # bỏ hệ số 0 ở bậc cao
        rem.pop()
    return q, rem

def interpolate(ys, domain):
    """Nội suy Lagrange: đa thức bậc < n đi qua (domain[i], ys[i])."""
    f = [0]
    for i, ri in enumerate(domain):
        Li, den = [1], 1
        for k, rk in enumerate(domain):
            if k != i:
                Li = poly_mul(Li, [mod(-rk), 1])
                den = mod(den * (ri - rk))
        f = poly_add(f, poly_scale(Li, ys[i] * inv(den)))
    return f

# Mỗi cột j của A, B, C → đa thức a_j(x), b_j(x), c_j(x)
def column_polys(M):
    return [interpolate([M[i][j] for i in range(n_constraints)], eval_domain)
            for j in range(n_vars)]
a_polys, b_polys, c_polys = column_polys(A), column_polys(B), column_polys(C)

# Vanishing polynomial Z_H(x) = (x-1)(x-2)(x-3)
Z = [1]
for r in eval_domain:
    Z = poly_mul(Z, [mod(-r), 1])

def qap_polys(s):
    """A(x) = Σ s_j·a_j(x), tương tự B(x), C(x); P(x) = A(x)B(x) - C(x)."""
    Ax, Bx, Cx = [0], [0], [0]
    for j in range(n_vars):
        Ax = poly_add(Ax, poly_scale(a_polys[j], s[j]))
        Bx = poly_add(Bx, poly_scale(b_polys[j], s[j]))
        Cx = poly_add(Cx, poly_scale(c_polys[j], s[j]))
    return Ax, Bx, Cx, poly_add(poly_mul(Ax, Bx), poly_scale(Cx, -1))

Ax, Bx, Cx, P = qap_polys(s)
h, rem = poly_divmod(P, Z)                    # h(x) = P(x) / Z_H(x)

print(f"\n=== BƯỚC 3: QAP (hệ số từ bậc thấp đến bậc cao) ===")
print(f"A(x) = {Ax}, B(x) = {Bx}, C(x) = {Cx}")
print(f"Z_H(x) = {Z}")
print(f"P(x) = A(x)B(x) - C(x) = {P}")
print(f"h(x) = {h}, dư = {rem} -> P chia hết cho Z_H: {rem == [0]}")

# ============================================================
# BƯỚC 4: Trusted Setup – chọn τ bí mật, công bố SRS
# ============================================================
random.seed(2016)
tau = random.randint(4, p - 1)                # τ không thuộc miền H
# Mô phỏng "trong số mũ": điểm [u]G được thay bằng chính số u.
# SRS = {[τ^i]G}, i = 0..n-1 (đủ cho A, B, C bậc ≤ n-1 và h bậc ≤ n-2)
srs = [pow(tau, i, p) for i in range(n_constraints)]
Z_tau = poly_eval(Z, tau)                     # vk: mô phỏng [Z_H(τ)]_2
print(f"\n=== BƯỚC 4: Setup ===")
print(f"τ (toxic waste) = {tau}, SRS = {srs}, Z_H(τ) = {Z_tau}")
del tau                                       # xóa toxic waste
