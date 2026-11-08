# Mã nguồn 4.12 - Mini-SNARK: tạo và xác minh proof, thử gian lận
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 177
# Trích tự động từ chapters/ch4/main.tex (dòng 4066) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.11 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_11_noi_suy_lagrange_chuyen_r1cs import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 5: Mini-SNARK Prove & Verify
# (Đơn giản hóa: không dùng pairing – dùng commitment trực tiếp)
# ============================================================

print(f"\n=== BƯỚC 5: Mini-SNARK ===")

# --- PROVE ---
# Prover tạo "proof" = (A(τ), B(τ), C(τ), H(τ))
# (Trong Groth16 thật, đây là điểm EC; ở đây dùng giá trị trực tiếp)
proof = {
    'A_tau': A_tau,
    'B_tau': B_tau,
    'C_tau': C_tau,
    'H_tau': H_tau,
}
print(f"Proof: {proof}")

# --- VERIFY ---
# Verifier biết: τ (qua SRS), Z_H, public input (out=35)
# Kiểm tra: A(τ)·B(τ) - C(τ) == H(τ)·Z_H(τ)
def mini_verify(proof, Z_tau, p):
    lhs = mod(proof['A_tau'] * proof['B_tau'] - proof['C_tau'])
    rhs = mod(proof['H_tau'] * Z_tau)
    return lhs == rhs

valid = mini_verify(proof, Z_tau, p)
print(f"Verify: {valid}")

# --- THỬ GIAN LẬN ---
# Prover gian lận: dùng witness sai (x=4)
print(f"\n--- Thử gian lận (x=4) ---")
x_fake = 4
s_fake = [1, 35, x_fake, mod(x_fake**2), mod(x_fake**3)]

A_fake = compute_qap_at_tau(A, s_fake, eval_domain, tau)
B_fake = compute_qap_at_tau(B, s_fake, eval_domain, tau)
C_fake = compute_qap_at_tau(C, s_fake, eval_domain, tau)
P_fake = mod(A_fake * B_fake - C_fake)

# Trong F_p, chia cho Z_H(τ) ≠ 0 luôn làm được, nên H_fake vẫn ra một số;
# chỗ sai nằm ở đa thức: P(x) không chia hết cho Z_H(x)
H_fake_attempt = mod(P_fake * inv(Z_tau))

fake_proof = {
    'A_tau': A_fake,
    'B_tau': B_fake,
    'C_tau': C_fake,
    'H_tau': H_fake_attempt,
}

# Verification vẫn "pass" tại τ cụ thể này (vì chưa có commitment)
# Nhưng trên đa thức, P(x) KHÔNG chia hết cho Z_H(x) – đây là nơi
# việc ẩn τ trong CRS (Prover không biết τ) ngăn gian lận.
print(f"P_fake(τ) = {P_fake}")
print(f"QUAN TRỌNG: Tại τ cụ thể, gian lận có thể 'lọt'.")
print(f"Groth16 thật ẩn τ trong CRS và dùng pairing để ngăn điều này:")
print(f"  Prover chỉ thấy [τ^i]G, không biết τ (qua trusted setup).")
print(f"  Nếu P(x) không chia hết cho Z_H(x), pairing check sẽ thất bại.")
