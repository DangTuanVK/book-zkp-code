# Mã nguồn 3.4 - Đo lường hiệu năng và phân tích tính zero-knowledge, soundness
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 3, trang 103
# Trích tự động từ chapters/ch3/main.tex (dòng 1005) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 3.2 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_3_02_schnorr_nizk_su_dung_bien import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# ĐO LƯỜNG HIỆU NĂNG VÀ PHÂN TÍCH
# ============================================================
import time

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

print(f"Tạo {n_proofs} proof:   {prove_time:.3f}s "
      f"({prove_time/n_proofs*1000:.1f} ms/proof)")
print(f"Verify {n_proofs} proof: {verify_time:.3f}s "
      f"({verify_time/n_proofs*1000:.1f} ms/proof)")
print(f"Tất cả valid: {all(results)}")

# Phân tích zero-knowledge: thống kê phân phối
print(f"\n--- Zero-Knowledge Analysis ---")
print(f"Thống kê z values từ 100 proof (nên phân phối đều):")
z_values = [pi[1] for pi in proofs]
from collections import Counter
z_counts = Counter(z_values)
print(f"  Số giá trị z khác nhau: {len(z_counts)} / {n_proofs}")
print(f"  (Nếu ~= {n_proofs}: phân phối đều → zero-knowledge)")

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
