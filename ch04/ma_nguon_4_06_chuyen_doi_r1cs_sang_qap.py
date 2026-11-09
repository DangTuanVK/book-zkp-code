# Mã nguồn 4.6 - Chuyển đổi R1CS sang QAP và kiểm tra tính chia hết cho Z_H(x)
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 153
# Trích tự động từ chapters/ch4/main.tex (dòng 2044) bằng extract.py; không sửa tay file này.

# === QAP từ R1CS: làm việc với ĐA THỨC, không chỉ giá trị tại một điểm ===
p = 41

# --- Phép toán đa thức trên F_p (hệ số từ bậc thấp đến bậc cao) ---
def poly_add(f, g):
    n = max(len(f), len(g))
    return [((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0)) % p
            for i in range(n)]

def poly_scale(f, c):
    return [(c * a) % p for a in f]

def poly_mul(f, g):
    r = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            r[i + j] = (r[i + j] + a * b) % p
    return r

def poly_divmod(f, g):
    """Chia f cho g, trả về (thương, dư)."""
    f = f[:]
    q = [0] * max(len(f) - len(g) + 1, 1)
    inv = pow(g[-1], p - 2, p)
    for i in range(len(f) - len(g), -1, -1):
        c = (f[i + len(g) - 1] * inv) % p
        q[i] = c
        for j, b in enumerate(g):
            f[i + j] = (f[i + j] - c * b) % p
    rem = f[:len(g) - 1]
    while len(rem) > 1 and rem[-1] == 0:   # bỏ hệ số 0 ở bậc cao
        rem.pop()
    return q, rem

def poly_eval(f, x):
    return sum(a * pow(x, i, p) for i, a in enumerate(f)) % p

def interpolate(xs, ys):
    """Nội suy Lagrange: đa thức bậc < len(xs) đi qua (xs[i], ys[i])."""
    result = [0]
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        Li, den = [1], 1
        for k, xk in enumerate(xs):
            if k != i:
                Li = poly_mul(Li, [-xk % p, 1])
                den = den * (xi - xk) % p
        result = poly_add(result, poly_scale(Li, yi * pow(den, p - 2, p)))
    return result

# --- R1CS cho x^3 + x + 5 = 35 (Mục 4.3), s = (1, out, x, w1, w2) ---
A = [[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [-5, 1, -1, 0, -1]]
B = [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]]
C = [[0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]
n, m = len(A), len(A[0])
rs = [1, 2, 3]                                    # điểm r_1, r_2, r_3

# Bước 1: nội suy từng cột thành đa thức a_j, b_j, c_j
a = [interpolate(rs, [A[i][j] % p for i in range(n)]) for j in range(m)]
b = [interpolate(rs, [B[i][j] % p for i in range(n)]) for j in range(m)]
c = [interpolate(rs, [C[i][j] % p for i in range(n)]) for j in range(m)]

Z = [1]                                           # Z_H(x) = (x-1)(x-2)(x-3)
for r in rs:
    Z = poly_mul(Z, [-r % p, 1])

def qap_polys(s):
    """Bước 2: A(x), B(x), C(x) từ assignment s; P = A*B - C."""
    Ax, Bx, Cx = [0], [0], [0]
    for j in range(m):
        Ax = poly_add(Ax, poly_scale(a[j], s[j]))
        Bx = poly_add(Bx, poly_scale(b[j], s[j]))
        Cx = poly_add(Cx, poly_scale(c[j], s[j]))
    return Ax, Bx, Cx, poly_add(poly_mul(Ax, Bx), poly_scale(Cx, -1))

def qap_check(s):
    """Bước 3: s thỏa QAP  <=>  P(x) chia hết cho Z_H(x) (dư bằng 0)."""
    *_, P = qap_polys(s)
    h, rem = poly_divmod(P, Z)
    return rem == [0], h, rem

ok, h, _ = qap_check([1, 35, 3, 9, 27])           # witness đúng, x = 3
print("Witness đúng (x=3): chia hết =", ok, "| h(x) =", h)
ok, _, rem = qap_check([1, 35, 4, 16, 64 % p])    # witness sai, x = 4
print("Witness sai  (x=4): chia hết =", ok, "| dư =", rem)
