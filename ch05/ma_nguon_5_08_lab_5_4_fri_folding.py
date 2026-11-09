# Mã nguồn 5.8 - Lab 5.4: FRI folding theo cặp (x, -x) trên coset L
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 253
# Trích tự động từ chapters/ch5/main.tex (dòng 3267) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.7 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_07_lab_5_3_xay_dung import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 4: FRI Folding – Giảm bậc đa thức
# ============================================================
def challenge(*data):
    """Thử thách Fiat-Shamir: băm dữ liệu đã cam kết, ra phần tử khác 0."""
    return int(hashlib.sha256(repr(data).encode()).hexdigest(), 16) % (p - 1) + 1

def fri_fold(vals, xs, beta):
    """Một vòng gấp. Miền xs đóng với phép đổi dấu: xs[j + h] = -xs[j].
    f'(x^2) = (f(x) + f(-x))/2 + beta * (f(x) - f(-x))/(2x)."""
    h = len(vals) // 2
    new_vals = [mod((vals[j] + vals[j + h]) * inv(2)
                    + beta * (vals[j] - vals[j + h]) * inv(2 * xs[j]))
                for j in range(h)]
    new_xs = [mod(x * x) for x in xs[:h]]            # miền mới: {x^2}
    return new_vals, new_xs

def fri_commit(vals, xs, rounds):
    """Pha commit: gấp `rounds` lần, cam kết Merkle mỗi tầng."""
    layers = [(vals, xs, build_merkle(vals))]
    betas = []
    for _ in range(rounds):
        beta = challenge("fri", layers[-1][2][0])       # băm root tầng trước
        vals, xs = fri_fold(vals, xs, beta)
        layers.append((vals, xs, build_merkle(vals)))
        betas.append(beta)
    return layers, betas

print("\n=== FRI Folding (f0 = t|L, bậc < 4) ===")
fri_layers, betas = fri_commit(tL, L, rounds=2)      # 16 -> 8 -> 4
for r, (vals, xs, (root, _)) in enumerate(fri_layers):
    note = f"beta={betas[r-1]}, " if r > 0 else ""
    print(f"  Tầng {r}: {note}{len(vals)} giá trị, root={root}")
    print(f"          {vals}")
final = fri_layers[-1][0]
print(f"  Tầng cuối hằng số? {len(set(final)) == 1}")
