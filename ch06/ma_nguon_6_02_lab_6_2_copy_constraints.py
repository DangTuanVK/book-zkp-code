# Mã nguồn 6.2 - Lab 6.2: Copy constraints và grand product permutation argument
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 6, trang 254
# Trích tự động từ chapters/ch6/main.tex (dòng 869) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 6.1 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_6_01_lab_6_1_xay_dung import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 4: Copy Constraints (Permutation)
# ============================================================
# Đánh số wire: (gate, col) → index
# Gate 1: a=0, b=1, c=2
# Gate 2: a=3, b=4, c=5
# Gate 3: a=6, b=7, c=8

# Copy constraints (cùng wire vật lý):
# - Wire 0 (G1.a=x) = Wire 1 (G1.b=x) = Wire 4 (G2.b=x)
# - Wire 2 (G1.c=w1) = Wire 3 (G2.a=w1)
# - Wire 5 (G2.c=out) = Wire 6 (G3.a=out)

# Permutation σ: wire i → wire j nếu cùng giá trị
# Biểu diễn dạng cycle:
# {0, 1, 4} (x), {2, 3} (w1), {5, 6} (out), {7} (0), {8} (0)
sigma = [1, 4, 3, 2, 0, 6, 5, 7, 8]
# σ(0)=1, σ(1)=4, σ(4)=0: cycle (0→1→4→0)
# σ(2)=3, σ(3)=2: cycle (2→3→2)
# σ(5)=6, σ(6)=5: cycle (5→6→5)

# Flatten wire values
wire_values = []
for row in wires:
    wire_values.extend(row)

print(f"\n=== Copy Constraints ===")
print(f"Wire values: {wire_values}")
print(f"Permutation σ: {sigma}")

# Kiểm tra: f[i] == f[σ(i)] cho mọi i
print(f"\nCopy constraint check:")
copy_ok = True
for i in range(len(sigma)):
    si = sigma[i]
    ok = wire_values[i] == wire_values[si]
    if i != si:  # Chỉ in copy constraints thực sự
        print(f"  wire[{i}]={wire_values[i]} == "
              f"wire[σ({i})={si}]={wire_values[si]} → "
              f"{'OK' if ok else 'FAIL'}")
    copy_ok &= ok
print(f"  All copies: {'PASS' if copy_ok else 'FAIL'}")

# ============================================================
# BƯỚC 5: Grand Product (Permutation Argument)
# ============================================================
beta = random.randint(1, p - 1)
gamma = random.randint(1, p - 1)

print(f"\n=== Grand Product (β={beta}, γ={gamma}) ===")

numerator_prod = 1
denominator_prod = 1
Z_acc = [1]  # Z[0] = 1

for i in range(len(wire_values)):
    f_i = wire_values[i]
    num_i = mod(f_i + beta * i + gamma)
    den_i = mod(f_i + beta * sigma[i] + gamma)
    numerator_prod = mod(numerator_prod * num_i)
    denominator_prod = mod(denominator_prod * den_i)
    Z_next = mod(numerator_prod * inv(denominator_prod))
    Z_acc.append(Z_next)

print(f"  Z accumulator: {Z_acc}")
print(f"  Z[n] = {Z_acc[-1]} (should be 1): "
      f"{'PASS' if Z_acc[-1] == 1 else 'FAIL'}")

# Thử phá copy constraint
print(f"\n--- Thử phá copy constraint ---")
bad_wires = wire_values[:]
bad_wires[4] = 5  # Đổi G2.b từ x=3 thành 5 (sai!)
print(f"Bad wire values: {bad_wires}")

num_bad, den_bad = 1, 1
for i in range(len(bad_wires)):
    num_bad = mod(num_bad * (bad_wires[i] + beta * i + gamma))
    den_bad = mod(den_bad * (bad_wires[i] + beta * sigma[i] + gamma))
Z_bad = mod(num_bad * inv(den_bad))
print(f"  Z[n] = {Z_bad} (should be 1): "
      f"{'PASS' if Z_bad == 1 else 'FAIL – PHÁT HIỆN GIAN LẬN'}")
