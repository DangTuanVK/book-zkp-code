# Mã nguồn 3.4 - Đo lường hiệu năng và phân tích tính zero-knowledge, soundness
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 3, trang 111
# Trích tự động từ chapters/ch3/main.tex (dòng 1167) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 3.2 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_3_02_schnorr_nizk_su_dung_bien import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# ĐO LƯỜNG HIỆU NĂNG VÀ PHÂN TÍCH
# ============================================================
import time
from collections import Counter

print(f"\n{'='*50}")
print(f"PHÂN TÍCH HIỆU NĂNG")
print(f"{'='*50}")

# Tạo và verify 100 proof
n_proofs = 100
start = time.time()
proofs = [schnorr_nizk_prove(G, H_public, x_secret, order)
          for _ in range(n_proofs)]
prove_time = time.time() - start

start = time.time()
results = [schnorr_nizk_verify(G, H_public, pi, order)
           for pi in proofs]
verify_time = time.time() - start

def ms_label(t):
    """Thời gian phụ thuộc máy, chỉ in độ lớn (ms/proof)."""
    ms = t / n_proofs * 1000
    return "< 1 ms/proof" if ms < 1 else f"~{ms:.0f} ms/proof"

print(f"Tạo {n_proofs} proof:   {ms_label(prove_time)}")
print(f"Verify {n_proofs} proof: {ms_label(verify_time)}")
print(f"Tất cả valid: {all(results)}")

# ------------------------------------------------------------
# Phân tích HVZK: so phân phối transcript thật với simulator
# ------------------------------------------------------------
def schnorr_simulate(G, H, order):
    """Simulator: không biết x, chọn (e, z) trước, tính a ngược."""
    e = random.randint(1, order - 1)
    z = random.randrange(order)
    a = z * G + (-(e * H))           # a = [z]G - [e]H
    return a, e, z

def real_transcript(G, H, x, order):
    """Transcript thật của giao thức tương tác, Verifier trung thực."""
    r = random.randrange(order)
    a = r * G
    e = random.randint(1, order - 1)
    return a, e, (r + e * x) % order

def transcript_ok(G, H, a, e, z):
    return z * G == a + (e * H)

def stat_distance(c1, c2, n):
    """Khoảng cách thống kê giữa hai phân phối thực nghiệm."""
    keys = set(c1) | set(c2)
    return sum(abs(c1[k] - c2[k]) for k in keys) / (2 * n)

print(f"\n--- Zero-Knowledge Analysis (HVZK) ---")
n_samples = 20000
real = [real_transcript(G, H_public, x_secret, order)
        for _ in range(n_samples)]
sim = [schnorr_simulate(G, H_public, order) for _ in range(n_samples)]
print(f"Simulator: mọi transcript đều hợp lệ: "
      f"{all(transcript_ok(G, H_public, *t) for t in sim)}")

z_real = Counter(t[2] for t in real)
z_sim = Counter(t[2] for t in sim)
print(f"  Số giá trị z khác nhau: thật {len(z_real)}, "
      f"giả {len(z_sim)} (tối đa {order})")
# So phân phối của cặp (a, e): mỗi cặp xác định duy nhất z
ae_real = Counter((str(t[0]), t[1]) for t in real)
ae_sim = Counter((str(t[0]), t[1]) for t in sim)
d_z = stat_distance(z_real, z_sim, n_samples)
d_ae = stat_distance(ae_real, ae_sim, n_samples)
print(f"  Khoảng cách thống kê (z):     {d_z:.3f}")
print(f"  Khoảng cách thống kê (a, e):  {d_ae:.3f}")
# Nhiễu lấy mẫu của hai mẫu đều cùng cỡ, để đối chiếu
u1 = Counter(random.randrange(order * (order - 1)) for _ in range(n_samples))
u2 = Counter(random.randrange(order * (order - 1)) for _ in range(n_samples))
print(f"  Nhiễu lấy mẫu (hai mẫu đều):  {stat_distance(u1, u2, n_samples):.3f}")

# Soundness test: thử brute-force tạo proof giả
print(f"\n--- Soundness Test ---")
n_attempts = 1000
n_lucky = 0
for _ in range(n_attempts):
    z_rand = random.randint(0, order - 1)
    a_rand = random.randint(1, order - 1) * G
    fake_proof = (a_rand, z_rand)
    if schnorr_nizk_verify(G, H_public, fake_proof, order):
        n_lucky += 1
print(f"Brute-force {n_attempts} proof ngẫu nhiên: "
      f"{n_lucky} accepted")
print(f"Xác suất: {n_lucky/n_attempts:.4f} "
      f"(expected ~1/{order} ≈ {1/order:.4f})")
