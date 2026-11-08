# Mã nguồn 4.8 - Pairing Tate trên đường cong tham số nhỏ: vòng lặp Miller (Thuật toán~refalg:miller-loop) và lũy thừa cuối (Thuật toán~refalg:final-exp); kiểm tra tính song tuyến tính
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 176
# Trích tự động từ chapters/ch4/main.tex (dòng 3489) bằng extract.py; không sửa tay file này.

# === Pairing Tate trên đường cong tham số nhỏ: vòng lặp Miller + lũy thừa cuối ===
# E: y^2 = x^3 + x trên F_p, p = 3 (mod 4): đường cong siêu kỳ dị, #E = p + 1,
# bậc nhúng k = 2, nên G_T nằm trong F_{p^2} = F_p[i] với i^2 = -1.
p, r = 40531, 10133                       # p + 1 = 4 r, r nguyên tố

# --- Trường F_{p^2}: phần tử (a, b) biểu diễn a + b i ---
def f2(a, b=0): return (a % p, b % p)
def add2(u, v): return f2(u[0] + v[0], u[1] + v[1])
def sub2(u, v): return f2(u[0] - v[0], u[1] - v[1])
def mul2(u, v): return f2(u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])
def pow2(u, e):
    res = f2(1)
    while e:
        if e & 1: res = mul2(res, u)
        u, e = mul2(u, u), e >> 1
    return res

# --- Phép toán điểm trên E(F_p); None là điểm vô cực O ---
def ec_add(P, Q):
    if P is None: return Q
    if Q is None: return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % p == 0: return None
    lam = ((3 * x1 * x1 + 1) * pow(2 * y1, p - 2, p) if P == Q
           else (y2 - y1) * pow(x2 - x1, p - 2, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    return (x3, (lam * (x1 - x3) - y1) % p)

def ec_mul(k, P):
    R = None
    while k:
        if k & 1: R = ec_add(R, P)
        P, k = ec_add(P, P), k >> 1
    return R

def distort(Q):                           # phi(x, y) = (-x, i y): đưa Q ra F_{p^2}
    return (f2(-Q[0]), f2(0, Q[1]))

def line(T, U, S):
    """Giá trị tại S của đường thẳng qua T, U (tiếp tuyến nếu T = U).
    Bỏ qua đường thẳng đứng (mẫu số): giá trị của chúng thuộc F_p
    và bị lũy thừa cuối triệt tiêu."""
    (xT, yT), (xU, yU) = T, U
    if xT == xU and (yT + yU) % p == 0:   # T + U = O: đường thẳng đứng
        return sub2(S[0], f2(xT))
    lam = ((3 * xT * xT + 1) * pow(2 * yT, p - 2, p) if T == U
           else (yU - yT) * pow(xU - xT, p - 2, p)) % p
    # l(S) = y_S - y_T - lam (x_S - x_T)
    return sub2(sub2(S[1], f2(yT)), mul2(f2(lam), sub2(S[0], f2(xT))))

# --- Pha 1: vòng lặp Miller, tính f_{r,P}(S) ---
def miller_loop(P, S):
    T, f = P, f2(1)
    for bit in bin(r)[3:]:                # duyệt bit của r, bỏ bit cao nhất
        f = mul2(mul2(f, f), line(T, T, S))   # nhân đôi: f <- f^2 * l_{T,T}(S)
        T = ec_add(T, T)
        if bit == "1":                        # cộng: f <- f * l_{T,P}(S)
            f = mul2(f, line(T, P, S))
            T = ec_add(T, P)
    return f

# --- Pha 2: lũy thừa cuối, đưa f về nhóm con cấp r của F_{p^2}^* ---
def final_exp(f):
    return pow2(f, (p * p - 1) // r)

def pairing(P, Q):
    return final_exp(miller_loop(P, distort(Q)))

# --- Tìm điểm sinh P cấp r ---
x = 2
while True:
    rhs = (x ** 3 + x) % p
    y = pow(rhs, (p + 1) // 4, p)         # căn bậc hai khi p = 3 (mod 4)
    if y * y % p == rhs:
        P = ec_mul(4, (x, y))             # nhân cofactor 4
        if P is not None: break
    x += 1
assert ec_mul(r, P) is None

g = pairing(P, P)
a, b = 1234, 5678
print("e(P, P)              =", g, "| khác 1:", g != f2(1))
print("e(P, P)^r            =", pow2(g, r), " (cấp r)")
print("Song tuyến tính      :", pairing(ec_mul(a, P), ec_mul(b, P)) == pow2(g, a * b))
print("e(aP, bP) = e(abP, P):", pairing(ec_mul(a, P), ec_mul(b, P))
      == pairing(ec_mul(a * b % r, P), P))
print("Bỏ lũy thừa cuối     :", miller_loop(ec_mul(a, P), distort(ec_mul(b, P)))
      == pow2(miller_loop(P, distort(P)), a * b), "(chưa duy nhất)")
