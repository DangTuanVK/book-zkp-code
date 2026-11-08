# Mã nguồn 5.2 - Chạy STARK từng bước trên F_97 với trace a^8, n = 4, N = 16: sinh mọi giá trị của Bảng~reftab:stark-walkthrough và Hình~reffig:stark-amplify
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 221
# Trích tự động từ chapters/ch5/main.tex (dòng 1737) bằng extract.py; không sửa tay file này.

# Chạy STARK từng bước với tham số nhỏ: F_97, trace a^8 (n = 4), |L| = 16
import hashlib

p, G = 97, 5                              # 5 là phần tử sinh của F_97^*
n, BLOWUP, Q = 4, 4, 2                    # 4 hàng trace, rho = 1/4, 2 query
N = n * BLOWUP
inv = lambda a: pow(a % p, p - 2, p)

def ev(f, x):                             # đánh giá đa thức (hệ số bậc thấp trước)
    r = 0
    for c in reversed(f):
        r = (r * x + c) % p
    return r

def interpolate(xs, ys):                  # nội suy Lagrange
    res = [0] * len(xs)
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        L_, den = [1], 1
        for k_, xk in enumerate(xs):
            if k_ != i:
                L_ = [(a - xk * b) % p for a, b in zip([0] + L_, L_ + [0])]
                den = den * (xi - xk) % p
        res = [(a + yi * inv(den) * b) % p for a, b in zip(res, L_)]
    return res

k = pow(G, (p - 1) // N, p); w = pow(k, BLOWUP, p)
H = [pow(w, i, p) for i in range(n)]                  # miền trace, cỡ 4
L = [G * pow(k, j, p) % p for j in range(N)]          # miền mở rộng, cỡ 16

h32 = lambda *xs: hashlib.sha256(repr(xs).encode()).hexdigest()
def merkle_root(vals):
    lay = [h32(v) for v in vals]
    while len(lay) > 1:
        lay = [h32(lay[i], lay[i + 1]) for i in range(0, len(lay), 2)]
    return lay[0][:8]                                 # in 8 ký tự hex đầu

class Transcript:                                     # Fiat-Shamir
    def __init__(s): s.st = "stark-f97"
    def absorb(s, *x): s.st = h32(s.st, *x)
    def challenge(s, avoid=()):
        while True:
            s.st = h32(s.st, "c"); c = int(s.st, 16) % p
            if c not in avoid and c != 0:
                return c

trace, y = [3, 9, 81, 62], 62                         # 3 -> 9 -> 81 -> 62 (mod 97)
tr = Transcript()
# 1. GHI: nội suy trên H, mở rộng sang L, cam kết
t = interpolate(H, trace); tL = [ev(t, x) for x in L]
rootT = merkle_root(tL); tr.absorb(rootT)
# 2. GỘP: ba ràng buộc (chuyển trạng thái, biên đầu, biên cuối)
a0, a1, a2 = tr.challenge(), tr.challenge(), tr.challenge()
def cp_at(tx, twx, x):
    Zt = (pow(x, n, p) - 1) * inv(x - H[-1]) % p
    return (a0 * (twx - tx * tx) * inv(Zt) + a1 * (tx - 3) * inv(x - 1)
            + a2 * (tx - y) * inv(x - H[-1])) % p
cpL = [cp_at(tL[j], tL[(j + BLOWUP) % N], L[j]) for j in range(N)]
cp = interpolate(L, cpL)
assert all(c == 0 for c in cp[n:])                    # CP có bậc < n
rootC = merkle_root(cpL); tr.absorb(rootC)
# 3. HỎI: điểm z ngoài H và L
z = tr.challenge(avoid=set(H) | set(L))
v = [ev(t, z), ev(t, w * z % p), ev(cp, z)]
assert v[2] == cp_at(v[0], v[1], z)                   # Verifier tự kiểm AIR tại z
tr.absorb(*v)
# 4. GẤP: đa thức DEEP và FRI 16 -> 8 -> 4
g0, g1, g2 = tr.challenge(), tr.challenge(), tr.challenge()
f0 = [(g0 * (tL[j] - v[0]) * inv(L[j] - z) + g1 * (tL[j] - v[1]) * inv(L[j] - w * z)
       + g2 * (cpL[j] - v[2]) * inv(L[j] - z)) % p for j in range(N)]
def fold(vals, xs, beta):
    h = len(vals) // 2
    return ([((vals[j] + vals[j + h]) * inv(2) + beta * (vals[j] - vals[j + h])
              * inv(2 * xs[j])) % p for j in range(h)], [x * x % p for x in xs[:h]])
b1 = tr.challenge(); f1, L1 = fold(f0, L, b1); tr.absorb(merkle_root(f1))
b2 = tr.challenge(); f2, L2 = fold(f1, L1, b2)
# 5. MỞ: vị trí query
tr.absorb(f2[0]); qs = [tr.challenge() % (N // 2) for _ in range(Q)]

print("H =", H, "  L =", L)
print("Ghi : trace =", trace, " t(X) =", t, " t|L =", tL, " root_T =", rootT)
print("Gộp : alpha =", (a0, a1, a2), " CP(X) =", cp[:n], " CP|L =", cpL, " root_C =", rootC)
print("Hỏi : z =", z, " t(z), t(wz), CP(z) =", v)
print("Gấp : gamma =", (g0, g1, g2), " f0 =", f0)
print("      beta1 =", b1, " f1 =", f1, " beta2 =", b2, " f2 =", f2)
print("Mở  : query j =", qs, " cặp vị trí:", [(j, j + N // 2) for j in qs])

# Khuếch đại lỗi: sửa một ô của trace
bad = [3, 9, 80, 62]
tb = interpolate(H, bad); tbL = [ev(tb, x) for x in L]
diffH = sum(a != b for a, b in zip(trace, bad))
diffL = sum(a != b for a, b in zip(tL, tbL))
print(f"Trace sai 1 ô: khác {diffH}/{n} điểm trên H, khác {diffL}/{N} điểm trên L")
print("t'|L =", tbL)
