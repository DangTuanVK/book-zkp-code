# Mã nguồn 4.12 - Mini-SNARK: Prover chỉ dùng SRS; gian lận thất bại vì phép chia còn dư, chỉ lọt khi tau bị lộ
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 189
# Trích tự động từ chapters/ch4/main.tex (dòng 4186) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.11 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_11_noi_suy_lagrange_chuyen_r1cs import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 5: Mini-SNARK Prove & Verify
# (Đơn giản hóa: không có pairing, không có α, β, δ; Prover
#  chỉ dùng SRS, KHÔNG biết τ)
# ============================================================
def commit(f):
    """[f(τ)] = Σ f_i·[τ^i]: tổ hợp tuyến tính của SRS, không cần τ."""
    return mod(sum(fi * srs[i] for i, fi in enumerate(f)))

def prove(s):
    Ax, Bx, Cx, P = qap_polys(s)
    h, rem = poly_divmod(P, Z)
    if rem != [0]:
        return None                           # không tồn tại đa thức h(x)
    return {'A': commit(Ax), 'B': commit(Bx), 'C': commit(Cx), 'h': commit(h)}

def verify(proof):
    # Verifier không biết τ, chỉ cần Z_H(τ) trong vk;
    # Groth16 kiểm tra đẳng thức này qua pairing, ở đây nhân trực tiếp.
    lhs = mod(proof['A'] * proof['B'] - proof['C'])
    return lhs == mod(proof['h'] * Z_tau)

print(f"\n=== BƯỚC 5: Mini-SNARK ===")
proof = prove(s)
print(f"Proof (witness đúng): {proof} -> verify = {verify(proof)}")

# --- THỬ GIAN LẬN: witness sai x = 4 ---
s_fake = [1, 35, 4, mod(4**2), mod(4**3)]
print(f"\n--- Thử gian lận (x=4) ---")
print(f"prove(s_fake) = {prove(s_fake)}")    # Prover trung thực từ chối
Af, Bf, Cf, P_fake = qap_polys(s_fake)
q, rem_fake = poly_divmod(P_fake, Z)
print(f"P_fake(x) / Z_H(x): thương = {q}, dư = {rem_fake}")

# Cách 1: bỏ phần dư, dùng thương q thay cho h. Tại τ, hai vế lệch
# nhau đúng rem_fake(τ), nên chỉ lọt khi τ là nghiệm của phần dư.
fake = {'A': commit(Af), 'B': commit(Bf), 'C': commit(Cf), 'h': commit(q)}
print(f"Cách 1 (dùng thương, bỏ dư): verify = {verify(fake)}")
roots = [t for t in range(4, p) if poly_eval(rem_fake, t) == 0]
print(f"  Số giá trị τ để cách 1 lọt: {len(roots)}/{p - 4}")

# Cách 2: cần đúng giá trị P_fake(τ)/Z_H(τ), mà muốn tính phải biết τ.
# Prover chỉ có [τ^i]G nên không làm được. Giả sử toxic waste bị lộ
# (trong mô phỏng, srs[1] bằng τ; với điểm thật [τ]G thì không):
tau_leaked = srs[1]
fake['h'] = mod(poly_eval(P_fake, tau_leaked) * inv(Z_tau))
print(f"Cách 2 (τ bị lộ, h = P_fake(τ)/Z_H(τ)): verify = {verify(fake)}")
