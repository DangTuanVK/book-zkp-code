# Mã nguồn 4.11 - Nội suy Lagrange chuyển R1CS sang QAP và kiểm tra
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 175
# Trích tự động từ chapters/ch4/main.tex (dòng 3988) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.10 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_10_pipeline_r1cs_va_witness_cho import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 3: R1CS → QAP (nội suy Lagrange)
# ============================================================

# Evaluation domain: r_1=1, r_2=2, r_3=3
eval_domain = [1, 2, 3]

def lagrange_poly_eval(values, domain, x_eval):
    """Nội suy Lagrange: cho giá trị tại domain, tính f(x_eval)."""
    n = len(values)
    result = 0
    for i in range(n):
        # L_i(x_eval)
        num, den = 1, 1
        for j in range(n):
            if i != j:
                num = mod(num * (x_eval - domain[j]))
                den = mod(den * (domain[i] - domain[j]))
        Li = mod(num * inv(den))
        result = mod(result + values[i] * Li)
    return result

# Nội suy mỗi cột → đa thức, sau đó tính A(τ), B(τ), C(τ)
def compute_qap_at_tau(matrix, s, domain, tau):
    """Tính Σ_j s_j · poly_j(τ) cho ma trận."""
    n = len(matrix)      # constraints
    m = len(matrix[0])   # variables
    total = 0
    for j in range(m):
        col = [matrix[i][j] for i in range(n)]
        pj_tau = lagrange_poly_eval(col, domain, tau)
        total = mod(total + s[j] * pj_tau)
    return total

# Tính vanishing polynomial Z_H(τ) = (τ-1)(τ-2)(τ-3)
def vanishing_at(tau, domain):
    result = 1
    for r in domain:
        result = mod(result * (tau - r))
    return result

# ============================================================
# BƯỚC 4: Trusted Setup – chọn τ bí mật
# ============================================================
tau = random.randint(4, p - 1)  # τ không trong eval domain

print(f"\n=== BƯỚC 3-4: QAP & Setup ===")
print(f"τ (toxic waste) = {tau}")

A_tau = compute_qap_at_tau(A, s, eval_domain, tau)
B_tau = compute_qap_at_tau(B, s, eval_domain, tau)
C_tau = compute_qap_at_tau(C, s, eval_domain, tau)
Z_tau = vanishing_at(tau, eval_domain)

# P(τ) = A(τ)·B(τ) - C(τ)
P_tau = mod(A_tau * B_tau - C_tau)

# H(τ) = P(τ) / Z_H(τ)
H_tau = mod(P_tau * inv(Z_tau))

print(f"A(τ) = {A_tau}")
print(f"B(τ) = {B_tau}")
print(f"C(τ) = {C_tau}")
print(f"Z_H(τ) = {Z_tau}")
print(f"P(τ) = A(τ)·B(τ) - C(τ) = {P_tau}")
print(f"H(τ) = P(τ)/Z_H(τ) = {H_tau}")

# Kiểm tra QAP: H(τ)·Z_H(τ) = P(τ)?
check = mod(H_tau * Z_tau) == P_tau
print(f"QAP check: H(τ)·Z_H(τ) = {mod(H_tau * Z_tau)} == P(τ)? {check}")
