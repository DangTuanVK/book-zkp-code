# Mã nguồn 4.13 - Phân tích tại sao witness sai bị phát hiện qua đa thức
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 178
# Trích tự động từ chapters/ch4/main.tex (dòng 4133) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.12 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_12_mini_snark_tao_va_xac import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 6: Phân tích – Tại sao witness sai bị phát hiện?
# ============================================================

print(f"\n=== Phân tích đa thức ===")

# Kiểm tra P(x) tại nhiều điểm (không chỉ τ)
print(f"P(x) tại evaluation domain (witness đúng, x=3):")
for r in eval_domain:
    A_r = compute_qap_at_tau(A, s, eval_domain, r)
    B_r = compute_qap_at_tau(B, s, eval_domain, r)
    C_r = compute_qap_at_tau(C, s, eval_domain, r)
    P_r = mod(A_r * B_r - C_r)
    print(f"  P({r}) = {P_r}")  # Phải = 0 tại mọi r trong domain

print(f"\nP(x) tại evaluation domain (witness SAI, x=4):")
for r in eval_domain:
    A_r = compute_qap_at_tau(A, s_fake, eval_domain, r)
    B_r = compute_qap_at_tau(B, s_fake, eval_domain, r)
    C_r = compute_qap_at_tau(C, s_fake, eval_domain, r)
    P_r = mod(A_r * B_r - C_r)
    print(f"  P({r}) = {P_r}")  # KHÔNG = 0 → P không chia hết cho Z_H

print(f"\nKẾT LUẬN:")
print(f"  Witness đúng → P(r_i) = 0 ∀i → Z_H | P → H(x) tồn tại ✓")
print(f"  Witness sai  → P(r_i) ≠ 0    → Z_H ∤ P → H(x) KHÔNG tồn tại ✗")
print(f"  → Schwartz-Zippel: kiểm tra tại τ ngẫu nhiên phát hiện gian lận")
print(f"    với xác suất ≥ 1 - deg(P)/p ≈ 1 - {2*n_constraints}/{p}")
