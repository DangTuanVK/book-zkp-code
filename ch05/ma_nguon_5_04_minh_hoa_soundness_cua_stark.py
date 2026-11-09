# Mã nguồn 5.4 - Minh họa soundness của STARK: một hàng sai trong trace buộc Prover chọn giữa bị FRI bác bỏ và trượt kiểm tra ràng buộc
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 243
# Trích tự động từ chapters/ch5/main.tex (dòng 2655) bằng extract.py; không sửa tay file này.

# === Soundness của STARK trên ví dụ nhỏ: AIR bình phương x_{i+1} = x_i^2 ===
import math
p = 257                                  # p - 1 = 256 = 2^8: có nhóm con cỡ 2^k
g = 3                                    # phần tử sinh của F_257^*
n, blowup = 8, 4                         # 8 hàng trace, tốc độ mã rho = 1/4

# --- Phép toán đa thức trên F_p (hệ số từ bậc thấp đến bậc cao) ---
def trim(f):
    while len(f) > 1 and f[-1] == 0:
        f = f[:-1]
    return f

def add(f, h):
    m = max(len(f), len(h))
    return trim([((f[i] if i < len(f) else 0) + (h[i] if i < len(h) else 0)) % p
                 for i in range(m)])

def mul(f, h):
    r = [0] * (len(f) + len(h) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(h):
            r[i + j] = (r[i + j] + a * b) % p
    return trim(r)

def divmod_poly(f, h):
    f, q = f[:], [0] * max(len(f) - len(h) + 1, 1)
    inv = pow(h[-1], p - 2, p)
    for i in range(len(f) - len(h), -1, -1):
        q[i] = f[i + len(h) - 1] * inv % p
        for j, b in enumerate(h):
            f[i + j] = (f[i + j] - q[i] * b) % p
    return trim(q), trim(f[:len(h) - 1] or [0])

def ev(f, x):
    return sum(a * pow(x, i, p) for i, a in enumerate(f)) % p

def interpolate(xs, ys):
    res = [0]
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        L, den = [1], 1
        for k, xk in enumerate(xs):
            if k != i:
                L, den = mul(L, [-xk % p, 1]), den * (xi - xk) % p
        res = add(res, [c * yi * pow(den, p - 2, p) % p for c in L])
    return res

# --- Miền: H (trace, cỡ n) và L = coset g*K (LDE, cỡ 4n), H nằm trong K ---
w = pow(g, (p - 1) // n, p)                      # căn nguyên thủy bậc n
H = [pow(w, i, p) for i in range(n)]
k = pow(g, (p - 1) // (n * blowup), p)           # căn nguyên thủy bậc 4n
L = [g * pow(k, i, p) % p for i in range(n * blowup)]   # rời H, đóng với nhân w

Zp = [1]                                         # Z_tr(x) = prod_{i<n-1} (x - w^i)
for h in H[:-1]:
    Zp = mul(Zp, [-h % p, 1])

def prover(trace):
    t = interpolate(H, trace)                        # đa thức trace, bậc < n
    tw = [c * pow(w, i, p) % p for i, c in enumerate(t)]   # t(w x)
    C = add(tw, [(-c) % p for c in mul(t, t)])       # C(x) = t(wx) - t(x)^2
    Q, R = divmod_poly(C, Zp)
    return t, C, Q, R

def spot_check(t, fQ, x):
    """Verifier kiểm tra tại x thuộc L: fQ(x) * Z_tr(x) == t(w x) - t(x)^2."""
    return fQ(x) * ev(Zp, x) % p == (ev(t, w * x % p) - ev(t, x) ** 2) % p

def degree_on_L(f):
    """Bậc của đa thức nội suy từ giá trị của f trên L (điều FRI kiểm tra)."""
    return len(interpolate(L, [f(x) for x in L])) - 1

honest = [3]
for _ in range(n - 1):
    honest.append(honest[-1] ** 2 % p)
cheat = honest[:]
cheat[5] = (cheat[5] + 1) % p                    # sửa một hàng: trace sai

for name, trace in (("Trace đúng", honest), ("Trace sai ", cheat)):
    t, C, Q, R = prover(trace)
    print(f"{name}: deg C = {len(C)-1}, dư khi chia Z_tr = {R}")

t, C, Q, R = prover(cheat)
# Chiến lược 1: gửi đúng thương C/Z_tr từng điểm -> qua mọi spot check, nhưng bậc cao
f1 = lambda x: ev(C, x) * pow(ev(Zp, x), p - 2, p) % p
ok1 = sum(spot_check(t, f1, x) for x in L)
print(f"Gian lận 1: qua {ok1}/{len(L)} spot check, bậc trên L = {degree_on_L(f1)}"
      f" (giới hạn {n-1}) -> FRI bác bỏ")
# Chiến lược 2: gửi thương Q bậc thấp, bỏ qua phần dư -> qua FRI, trượt spot check
f2 = lambda x: ev(Q, x)
ok2 = sum(spot_check(t, f2, x) for x in L)
print(f"Gian lận 2: bậc = {degree_on_L(f2)}, qua {ok2}/{len(L)} spot check"
      f" (cận lý thuyết {len(R)-1}/{len(L)})")

# --- Số query FRI cho 128 bit bảo mật, theo ba chế độ phân tích ---
print("\nrho    | duy nhất (1-rho)/2 | Johnson 1-sqrt(rho) | giả thuyết 1-rho")
for rho in (1/2, 1/4, 1/8, 1/16):
    # làm tròn 9 chữ số trước khi lấy trần: tránh sai số dấu phẩy động (256.0000001)
    qs = [math.ceil(round(128 / -math.log2(1 - d), 9))
          for d in ((1 - rho) / 2, 1 - math.sqrt(rho), 1 - rho)]
    print(f"1/{round(1/rho):<4} | {qs[0]:>18} | {qs[1]:>19} | {qs[2]:>16}")
