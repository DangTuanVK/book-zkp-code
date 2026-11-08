# Mã nguồn 6.3 - Lab 6.3: So sánh R1CS và PLONKish cho cùng bài toán
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 6, trang 272
# Trích tự động từ chapters/ch6/main.tex (dòng 1027) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 6.2 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_6_02_lab_6_2_copy_constraints import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 6: So sánh R1CS vs PLONKish cho cùng bài toán
# ============================================================

print(f"\n{'='*55}")
print(f"SO SÁNH: R1CS vs PLONKish cho x^2 + x = 12")
print(f"{'='*55}")

# R1CS: cần ma trận A, B, C
# Biến: s = [1, out, x, w1]
# RC1: x * x = w1        → A=[0,0,1,0], B=[0,0,1,0], C=[0,0,0,1]
# RC2: (x + w1) * 1 = out → A=[0,0,1,1], B=[1,0,0,0], C=[0,1,0,0]
# (out = 12 là public input, gán trực tiếp trong vector s)
print(f"\nR1CS:")
print(f"  Biến: s = [1, out, x, w1] = [1, 12, 3, 9]")
print(f"  Ràng buộc: 2 (1 nhân + 1 output check)")
print(f"  Ma trận: 2×4 × 3 = 24 phần tử")
print(f"  Wire connections: implicit trong ma trận")

# PLONKish: gate table + permutation
print(f"\nPLONKish:")
print(f"  Gate table: 3 hàng × (3 wire + 5 selector) = 24 phần tử")
print(f"  Permutation: σ = {sigma}")
print(f"  Wire connections: explicit permutation + grand product")
print(f"  Ưu điểm: universal setup, custom gates, lookup")

print(f"\nKết luận:")
print(f"  R1CS: đơn giản hơn, proof nhỏ hơn (Groth16)")
print(f"  PLONKish: linh hoạt hơn, universal setup, custom gates")
print(f"  Cùng bài toán nhỏ → khác biệt ít")
print(f"  Bài toán lớn (zkEVM) → PLONKish + lookup thắng rõ")
