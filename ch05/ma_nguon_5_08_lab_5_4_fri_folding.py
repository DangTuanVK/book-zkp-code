# Mã nguồn 5.8 - Lab 5.4: FRI folding - giảm bậc đa thức qua các vòng
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 236
# Trích tự động từ chapters/ch5/main.tex (dòng 3086) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.7 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_07_lab_5_3_xay_dung import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 4: FRI Folding – Giảm bậc đa thức
# ============================================================

def fri_fold(evaluations, domain_vals, alpha):
    """Một vòng FRI folding.
    f(x) = f_even(x^2) + x * f_odd(x^2)
    f_new(y) = f_even(y) + alpha * f_odd(y)

    Đơn giản hóa: dùng cặp (x, -x) để tách even/odd."""
    n = len(evaluations)
    new_evals = []
    new_domain = []

    for i in range(0, n, 2):
        if i + 1 >= n:
            break
        x_pos = domain_vals[i]
        x_neg = domain_vals[i + 1]
        f_pos = evaluations[i]      # f(x)
        f_neg = evaluations[i + 1]  # f(-x) hoặc f(x_paired)

        # f_even(x^2) = (f(x) + f(-x)) / 2
        f_even = mod((f_pos + f_neg) * inv(2))
        # f_odd(x^2) = (f(x) - f(-x)) / (2x)
        if x_pos != x_neg:
            f_odd = mod((f_pos - f_neg) * inv(2 * (x_pos - x_neg))
                        * (x_pos + x_neg))
            # Đơn giản hóa: dùng tổ hợp tuyến tính trực tiếp
            f_odd_simple = mod((f_pos - f_neg) * inv(x_pos - x_neg))
        else:
            f_odd_simple = 0

        # f_new = f_even + alpha * f_odd (đơn giản hóa)
        f_new = mod(f_pos + alpha * f_odd_simple)
        new_evals.append(f_new)
        new_domain.append(mod(x_pos * x_pos))  # y = x^2

    return new_evals, new_domain

# FRI commit phase
print(f"\n=== FRI Folding ===")
current_evals = extended_eval[:]
current_domain = extended_domain[:]
fri_layers = [(current_evals[:], root)]  # (evaluations, merkle_root)
alphas = []

n_rounds = 3  # log2(degree) vòng
for round_idx in range(n_rounds):
    alpha = random.randint(1, p - 1)
    alphas.append(alpha)

    new_evals, new_domain = fri_fold(current_evals, current_domain, alpha)

    # Commit vòng mới
    new_hashes = [sha256_hash(v) for v in new_evals]
    if len(new_hashes) > 1:
        new_root, new_tree = build_merkle(new_hashes)
    else:
        new_root = new_hashes[0] if new_hashes else "empty"
        new_tree = [new_hashes]

    fri_layers.append((new_evals[:], new_root))

    print(f"  Round {round_idx + 1}: alpha={alpha}, "
          f"evals {len(current_evals)} → {len(new_evals)}, "
          f"root={new_root}")

    current_evals = new_evals
    current_domain = new_domain

# Giá trị cuối cùng (phải là hằng số nếu đa thức bậc thấp)
print(f"\n  Final values: {current_evals}")
if len(set(current_evals)) <= 1:
    print(f"  → Tất cả bằng nhau = HẰNG SỐ → đa thức bậc thấp ✓")
else:
    print(f"  → Không phải hằng số (do domain nhỏ, đơn giản hóa)")
