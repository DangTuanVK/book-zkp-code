# Mã nguồn 6.2 - Lab 6.2: Copy constraints và grand product permutation argument
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 6, trang 273
# Trích tự động từ chapters/ch6/main.tex (dòng 959) bằng extract.py; không sửa tay file này.

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
# Cố định hạt giống để kết quả chạy tái lập được
rng = random.Random(2026)

def factors(values, beta, gamma):
    # Thừa số tử số (f_i + β·i + γ) và mẫu số (f_i + β·σ(i) + γ)
    nums = [mod(values[i] + beta * i + gamma) for i in range(len(values))]
    dens = [mod(values[i] + beta * sigma[i] + gamma)
            for i in range(len(values))]
    return nums, dens

def sample_challenges(values):
    # Chọn (β, γ) ngẫu nhiên; chọn lại nếu có thừa số bằng 0.
    # Với p = 41, khoảng 20% cặp (β, γ) làm một thừa số bằng 0
    # (mẫu số 0 thì không nghịch đảo được). Với p cỡ 2^254 như
    # PLONK thực tế, xác suất này không đáng kể.
    while True:
        beta = rng.randint(1, p - 1)
        gamma = rng.randint(1, p - 1)
        nums, dens = factors(values, beta, gamma)
        if 0 not in nums and 0 not in dens:
            return beta, gamma

beta, gamma = sample_challenges(wire_values)
print(f"\n=== Grand Product (β={beta}, γ={gamma}) ===")

numerator_prod = 1
denominator_prod = 1
Z_acc = [1]  # Z[0] = 1

nums, dens = factors(wire_values, beta, gamma)
for num_i, den_i in zip(nums, dens):
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

num_bad, den_bad = factors(bad_wires, beta, gamma)
if 0 in den_bad:
    print("  Mẫu số bằng 0 → bác bỏ proof")
else:
    Z_bad = 1
    for n_i, d_i in zip(num_bad, den_bad):
        Z_bad = mod(Z_bad * n_i * inv(d_i))
    print(f"  Z[n] = {Z_bad} (should be 1): "
          f"{'PASS' if Z_bad == 1 else 'FAIL – PHÁT HIỆN GIAN LẬN'}")
