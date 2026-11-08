# Mã nguồn 4.9 - Mô phỏng Groth16 trong số mũ: khi gamma = delta, proof cho out = 35 bị sửa thành proof hợp lệ cho out = 36
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 180
# Trích tự động từ chapters/ch4/main.tex (dòng 3713) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.6 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_06_chuyen_doi_r1cs_sang_qap import *  # noqa
# --- Hết phần thêm ---

# === Groth16 "trong số mũ": vì sao gamma phải khác delta ===
# Dùng lại p, a, b, c, Z, qap_polys, poly_divmod, poly_eval ở Mã nguồn 4.6
# (QAP cho x^3 + x + 5 = 35, s = (1, out, x, w1, w2)).
import random
ell = 1                                    # public input: s_1 = out

def setup(same_gamma_delta=False):
    tau, alpha, beta, gamma, delta = (random.randrange(1, p) for _ in range(5))
    if same_gamma_delta:
        gamma = delta                      # cấu hình SAI: gamma = delta
    inv = lambda u: pow(u, p - 2, p)
    L = [(beta * poly_eval(a[j], tau) + alpha * poly_eval(b[j], tau)
          + poly_eval(c[j], tau)) % p for j in range(m)]
    pk = dict(tau=tau, alpha=alpha, beta=beta, delta=delta,
              L_delta=[L[j] * inv(delta) % p for j in range(ell + 1, m)])
    vk = dict(alpha=alpha, beta=beta, gamma=gamma, delta=delta,
              L_gamma=[L[j] * inv(gamma) % p for j in range(ell + 1)])
    return pk, vk

def prove(pk, s):
    Ax, Bx, Cx, P = qap_polys(s)
    h, rem = poly_divmod(P, Z)
    assert rem == [0], "witness sai"
    t, d = pk["tau"], pk["delta"]
    r, s_ = random.randrange(p), random.randrange(p)
    piA = (pk["alpha"] + poly_eval(Ax, t) + r * d) % p
    piB = (pk["beta"] + poly_eval(Bx, t) + s_ * d) % p
    hZ_d = poly_eval(h, t) * poly_eval(Z, t) * pow(d, p - 2, p)
    piC = (sum(s[ell + 1 + k] * Lk for k, Lk in enumerate(pk["L_delta"]))
           + hZ_d + s_ * piA + r * piB - r * s_ * d) % p
    return piA, piB, piC

def verify(vk, x, proof):
    piA, piB, piC = proof
    sx = [1] + x                           # s_0 = 1, s_1..s_ell = x
    I = sum(sj * Lj for sj, Lj in zip(sx, vk["L_gamma"])) % p
    return piA * piB % p == (vk["alpha"] * vk["beta"] + I * vk["gamma"]
                             + piC * vk["delta"]) % p

def forge(vk, x_old, x_new, proof):
    """Đổi statement chỉ bằng vk: cộng sum (x_j - x'_j) [L_j/gamma]_1 vào pi_C."""
    piA, piB, piC = proof
    for j in range(1, ell + 1):
        piC += (x_old[j - 1] - x_new[j - 1]) * vk["L_gamma"][j]
    return piA, piB, piC % p

random.seed(2016)
s = [1, 35, 3, 9, 27]                      # witness đúng: x = 3, out = 35
for same in (False, True):
    pk, vk = setup(same_gamma_delta=same)
    pi = prove(pk, s)
    fake = forge(vk, [35], [36], pi)
    print(f"gamma {'= ' if same else '!='} delta: "
          f"verify(out=35) = {verify(vk, [35], pi)} | "
          f"proof giả cho out=36: {verify(vk, [36], fake)}")
