# Mã nguồn 5.6 - Lab 5.2: Nội suy trace thành đa thức bằng Lagrange
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 233
# Trích tự động từ chapters/ch5/main.tex (dòng 2986) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.5 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_05_lab_5_1_tao_execution import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 2: Nội suy trace → đa thức t(x)
# ============================================================
# Domain đơn giản: {1, 2, 3, 4}
domain = [1, 2, 3, 4]

def lagrange_eval(values, dom, x_eval):
    """Nội suy Lagrange: f(x_eval) từ [(dom[i], values[i])]."""
    n = len(values)
    result = 0
    for i in range(n):
        num, den = 1, 1
        for j in range(n):
            if i != j:
                num = mod(num * (x_eval - dom[j]))
                den = mod(den * (dom[i] - dom[j]))
        Li = mod(num * inv(den))
        result = mod(result + values[i] * Li)
    return result

# Kiểm tra nội suy đúng
print(f"\n=== Nội suy Lagrange ===")
for i, r in enumerate(domain):
    val = lagrange_eval(trace, domain, r)
    print(f"  t({r}) = {val}, expected {trace[i]}, "
          f"{'OK' if val == trace[i] else 'FAIL'}")

# Tính t(x) trên domain mở rộng (blow-up factor = 4)
blowup = 4
extended_domain = list(range(1, len(trace) * blowup + 1))
extended_eval = [lagrange_eval(trace, domain, x)
                 for x in extended_domain]
print(f"\nExtended evaluation ({len(extended_domain)} điểm):")
for i, x in enumerate(extended_domain):
    print(f"  t({x}) = {extended_eval[i]}", end="")
    if x in domain:
        idx = domain.index(x)
        print(f"  ← trace[{idx}]", end="")
    print()
