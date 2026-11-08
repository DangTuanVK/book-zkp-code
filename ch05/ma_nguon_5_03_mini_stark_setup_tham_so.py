# Mã nguồn 5.3 - Mini-STARK: Setup (tham số), Prove và Verify với LDE, đa thức hợp thành, DEEP, FRI, grinding và Fiat-Shamir
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 215
# Trích tự động từ chapters/ch5/main.tex (dòng 1829) bằng extract.py; không sửa tay file này.

# === Mini-STARK: chứng minh "x_{i+1} = x_i^2, x_0 = 3" qua n bước ===
# Không zero-knowledge, tham số nhỏ: chỉ để minh họa các bước của thuật toán.
import hashlib

p = 2**64 - 2**32 + 1                     # trường Goldilocks
G = 7                                     # phần tử sinh của F_p^*
n, BLOWUP, Q, GRIND = 8, 4, 8, 8          # hàng trace, 1/rho, số query, bit grinding
N = n * BLOWUP
inv = lambda a: pow(a, p - 2, p)

# --- Đa thức (hệ số từ bậc thấp đến bậc cao) ---
def ev(f, x):
    r = 0
    for c in reversed(f):
        r = (r * x + c) % p
    return r

def mul(f, h):
    r = [0] * (len(f) + len(h) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(h):
            r[i + j] = (r[i + j] + a * b) % p
    return r

def interpolate(xs, ys):
    res = [0] * len(xs)
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        L, den = [1], 1
        for k, xk in enumerate(xs):
            if k != i:
                L, den = mul(L, [-xk % p, 1]), den * (xi - xk) % p
        c = yi * inv(den) % p
        res = [(a + c * b) % p for a, b in zip(res, L)]
    return res

# --- Miền: H = <w> cỡ n, L = G * <k> cỡ N (coset rời H); w * x_j = x_{j+BLOWUP} ---
k = pow(G, (p - 1) // N, p)
w = pow(k, BLOWUP, p)
H = [pow(w, i, p) for i in range(n)]
L = [G * pow(k, j, p) % p for j in range(N)]

def Zt(x):                                # triệt tiêu trên H \ {w^{n-1}}
    return (pow(x, n, p) - 1) * inv(x - H[-1]) % p

def air(t_x, t_wx, x, a0, a1):            # đa thức hợp thành tại một điểm
    trans = (t_wx - t_x * t_x) * inv(Zt(x)) % p     # ràng buộc chuyển trạng thái
    bound = (t_x - 3) * inv(x - 1) % p              # ràng buộc biên t(1) = 3
    return (a0 * trans + a1 * bound) % p

# --- Merkle và transcript Fiat-Shamir ---
H256 = lambda *xs: hashlib.sha256(b"".join(
    x if isinstance(x, bytes) else x.to_bytes(32, "big") for x in xs)).digest()

def merkle(vals):
    layers = [[H256(v) for v in vals]]
    while len(layers[-1]) > 1:
        a = layers[-1]
        layers.append([H256(a[i], a[i + 1]) for i in range(0, len(a), 2)])
    return layers

def path(layers, i):
    out = []
    for lay in layers[:-1]:
        out.append(lay[i ^ 1]); i //= 2
    return out

def check_path(root, i, v, pth):
    h = H256(v)
    for s in pth:
        h = H256(h, s) if i % 2 == 0 else H256(s, h)
        i //= 2
    return h == root

class Transcript:
    def __init__(self, statement):
        self.s = H256(b"mini-stark", statement)
    def absorb(self, *xs):
        self.s = H256(self.s, *xs)
    def challenge(self):
        self.s = H256(self.s, b"c")
        return int.from_bytes(self.s, "big") % p

def fold(vals, xs, beta):                 # một vòng gấp của FRI
    h = len(vals) // 2
    return ([((vals[j] + vals[j + h]) * inv(2) + beta * (vals[j] - vals[j + h])
              * inv(2 * xs[j])) % p for j in range(h)],
            [x * x % p for x in xs[:h]])

# ============================== PROVE ==============================
def prove(trace, y, fake_ood=False):
    tr = Transcript(y.to_bytes(32, "big"))              # phát biểu: x_{n-1} = y
    t = interpolate(H, trace)                           # 1. nội suy trace trên H
    tL = [ev(t, x) for x in L]                          # 2. LDE trên L
    T_tree = merkle(tL); tr.absorb(T_tree[-1][0])       # 3. cam kết trace
    a0, a1, a2 = tr.challenge(), tr.challenge(), tr.challenge()
    cpL = [(air(tL[j], tL[(j + BLOWUP) % N], L[j], a0, a1)      # 4. hợp thành
            + a2 * (tL[j] - y) * inv(L[j] - H[-1])) % p for j in range(N)]
    cp = interpolate(L, cpL)[:n]                        # Prover trung thực: bậc < n
    cpL = [ev(cp, x) for x in L]                        # (trace sai: bỏ phần bậc cao)
    C_tree = merkle(cpL); tr.absorb(C_tree[-1][0])      # 5. cam kết hợp thành
    z = tr.challenge()                                  # 6. điểm ngoài miền (DEEP)
    ood = [ev(t, z), ev(t, w * z % p), ev(cp, z)]
    if fake_ood:                                        # gian lận: sửa giá trị tại z
        ood[2] = (air(ood[0], ood[1], z, a0, a1)
                  + a2 * (ood[0] - y) * inv(z - H[-1])) % p
    tr.absorb(*ood)
    g0, g1, g2 = tr.challenge(), tr.challenge(), tr.challenge()
    fL = [(g0 * (tL[j] - ood[0]) * inv(L[j] - z)        # 7. đa thức DEEP
           + g1 * (tL[j] - ood[1]) * inv(L[j] - w * z)
           + g2 * (cpL[j] - ood[2]) * inv(L[j] - z)) % p for j in range(N)]
    vals, xs, fri = fL, L, []                           # 8. FRI: pha commit
    while len(vals) > BLOWUP:
        beta = tr.challenge()
        vals, xs = fold(vals, xs, beta)
        if len(vals) > BLOWUP:
            fri.append((vals, merkle(vals))); tr.absorb(fri[-1][1][-1][0])
    final = vals[0]; tr.absorb(final)
    nonce = 0                                           # 9. grinding
    while int.from_bytes(H256(tr.s, nonce)[:2], "big") >> (16 - GRIND):
        nonce += 1
    tr.absorb(nonce)
    opens = []                                          # 10. pha query
    for _ in range(Q):
        j = tr.challenge() % (N // 2)
        pos = [j, j + N // 2, (j + BLOWUP) % N, (j + N // 2 + BLOWUP) % N]
        o = {"t": [(tL[i], path(T_tree, i)) for i in pos],
             "cp": [(cpL[i], path(C_tree, i)) for i in pos[:2]], "fri": []}
        for vals_r, tree in fri:
            h = len(vals_r) // 2; jj = j % h
            o["fri"].append([(vals_r[i], path(tree, i)) for i in (jj, jj + h)])
        opens.append(o)
    return dict(T=T_tree[-1][0], C=C_tree[-1][0], ood=ood,
                fri=[tree[-1][0] for _, tree in fri],
                final=final, nonce=nonce, opens=opens)

# ============================== VERIFY ==============================
def verify(y, pi):
    tr = Transcript(y.to_bytes(32, "big"))              # 1. tái tạo thử thách
    tr.absorb(pi["T"]); a0, a1, a2 = tr.challenge(), tr.challenge(), tr.challenge()
    tr.absorb(pi["C"]); z = tr.challenge()
    t_z, t_wz, cp_z = pi["ood"]
    if cp_z != (air(t_z, t_wz, z, a0, a1)               # 2. kiểm tra AIR tại z
                + a2 * (t_z - y) * inv(z - H[-1])) % p:
        return "từ chối: AIR sai tại điểm ngoài miền"
    tr.absorb(*pi["ood"]); g0, g1, g2 = tr.challenge(), tr.challenge(), tr.challenge()
    betas, roots = [], list(pi["fri"])
    for r in range(len(roots) + 1):
        betas.append(tr.challenge())
        if r < len(roots):
            tr.absorb(roots[r])
    tr.absorb(pi["final"])
    if int.from_bytes(H256(tr.s, pi["nonce"])[:2], "big") >> (16 - GRIND):
        return "từ chối: grinding sai"
    tr.absorb(pi["nonce"])
    for o in pi["opens"]:
        j = tr.challenge() % (N // 2)
        pos = [j, j + N // 2, (j + BLOWUP) % N, (j + N // 2 + BLOWUP) % N]
        for i, (v, pth) in zip(pos, o["t"]):            # 3. Merkle của trace
            if not check_path(pi["T"], i, v, pth):
                return "từ chối: Merkle trace sai"
        for i, (v, pth) in zip(pos[:2], o["cp"]):
            if not check_path(pi["C"], i, v, pth):
                return "từ chối: Merkle hợp thành sai"
        tv = [v for v, _ in o["t"]]; cv = [v for v, _ in o["cp"]]
        pair = []                                       # 4. tính f tại x và -x
        for a, b, x in ((0, 2, L[j]), (1, 3, L[j + N // 2])):
            pair.append((g0 * (tv[a] - t_z) * inv(x - z)
                         + g1 * (tv[a] - t_wz) * inv(x - w * z)
                         + g2 * (cv[a] - cp_z) * inv(x - z)) % p)
        x, jj = L[j], j                                 # 5. kiểm tra chuỗi gấp FRI
        for r in range(len(roots) + 1):
            folded = ((pair[0] + pair[1]) * inv(2)
                      + betas[r] * (pair[0] - pair[1]) * inv(2 * x)) % p
            x = x * x % p
            if r == len(roots):
                if folded != pi["final"]:
                    return "từ chối: FRI tầng cuối sai"
                break
            h = (N >> (r + 1)) // 2; jj %= h
            (v0, p0), (v1, p1) = o["fri"][r]
            if not (check_path(roots[r], jj, v0, p0)
                    and check_path(roots[r], jj + h, v1, p1)):
                return "từ chối: Merkle FRI sai"
            if folded != (v0 if j % (2 * h) < h else v1):
                return "từ chối: FRI không nhất quán"
            pair = [v0, v1]
            if j % (2 * h) >= h:
                x = (-x) % p
    return "chấp nhận"

# ============================== DEMO ==============================
honest = [3]
for _ in range(n - 1):
    honest.append(honest[-1] ** 2 % p)
y = honest[-1]
pi = prove(honest, y)
size = sum(len(pth) * 32 + 8 for o in pi["opens"] for grp in (o["t"], o["cp"])
           for _, pth in grp) + sum(len(pth) * 32 + 8 for o in pi["opens"]
           for lay in o["fri"] for _, pth in lay)
print(f"Trace: {honest[:4]} ...  y = x_{n-1} = {y}")
print(f"[1] Trace đúng            -> {verify(y, pi)}  (proof ~{size} byte)")
print(f"[2] Sai phát biểu (y + 1) -> {verify(y + 1, pi)}")
bad = honest[:]; bad[5] = (bad[5] + 1) % p
print(f"[3] Trace sai một hàng    -> {verify(y, prove(bad, y))}")
print(f"[4] Trace sai, sửa OOD    -> {verify(y, prove(bad, y, fake_ood=True))}")
v, pth = pi["opens"][0]["t"][0]
pi["opens"][0]["t"][0] = ((v + 1) % p, pth)            # sửa một giá trị đã mở
print(f"[5] Sửa một giá trị mở    -> {verify(y, pi)}")
