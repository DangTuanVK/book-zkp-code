# Mã nguồn 4.1 - Hệ ràng buộc, lỗi thiếu ràng buộc và mẫu IsZero
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 125
# Trích tự động từ chapters/ch4/main.tex (dòng 558) bằng extract.py; không sửa tay file này.

# === Ràng buộc = phương trình đa thức P(z) = 0 trên F_p ===
p = 97  # Trường nhỏ cho dễ đọc

def satisfies(constraints, z):
    """Assignment z thỏa hệ ràng buộc nếu MỌI P_i(z) = 0 (mod p)."""
    return all(P(z) % p == 0 for P in constraints)

# --- Ví dụ 1: circuit a*b + a = 7, biến z = (a, b, m, y) ---
circuit = [
    lambda z: z['m'] - z['a'] * z['b'],   # cổng nhân: m = a*b
    lambda z: z['y'] - z['m'] - z['a'],   # cổng cộng: y = m + a
    lambda z: z['y'] - 7,                 # output công khai: y = 7
]
print("a=1, b=6:", satisfies(circuit, {'a': 1, 'b': 6, 'm': 6, 'y': 7}))
print("a=3, b=2:", satisfies(circuit, {'a': 3, 'b': 2, 'm': 6, 'y': 9}))

# --- Ví dụ 2: kiểm tra x < 4 bằng hai bit b0, b1 ---
# Ràng buộc tái hợp (tuyến tính): x = b0 + 2*b1
recompose = lambda z: z['x'] - z['b0'] - 2 * z['b1']
# Ràng buộc bit: b*(1-b) = 0  <=>  b thuộc {0, 1}
bit0 = lambda z: z['b0'] * (1 - z['b0'])
bit1 = lambda z: z['b1'] * (1 - z['b1'])

thieu = [recompose]                # QUÊN ràng buộc bit
du    = [recompose, bit0, bit1]    # Đầy đủ

# Prover gian lận: x = 50 (không nhỏ hơn 4), chọn b0 = 50, b1 = 0
gian_lan = {'x': 50, 'b0': 50, 'b1': 0}
# Prover trung thực: x = 3 = 1 + 2*1
trung_thuc = {'x': 3, 'b0': 1, 'b1': 1}

print("\nThiếu ràng buộc, x=50:", satisfies(thieu, gian_lan))  # True -> lỗ hổng!
print("Đầy đủ,         x=50:", satisfies(du, gian_lan))         # False
print("Đầy đủ,         x=3 :", satisfies(du, trung_thuc))       # True

# --- Ví dụ 3: IsZero, out = 1 nếu a = 0, ngược lại out = 0 ---
# Witness phụ u (Prover tự tính: u = a^{-1} nếu a != 0, tùy ý nếu a = 0)
is_zero = [
    lambda z: z['out'] - (1 - z['a'] * z['u']),  # out = 1 - a*u
    lambda z: z['a'] * z['out'],                 # a * out = 0
]
def prover_is_zero(a):
    u = pow(a, p - 2, p) if a % p else 0         # nghịch đảo Fermat
    return {'a': a, 'u': u, 'out': (1 - a * u) % p}

print()
for a in [0, 5]:
    z = prover_is_zero(a)
    print(f"IsZero({a}) = {z['out']}, hợp lệ: {satisfies(is_zero, z)}")
# Gian lận: a = 5 nhưng khai out = 1 -> không tồn tại u nào thỏa
cheat = [satisfies(is_zero, {'a': 5, 'u': u, 'out': 1}) for u in range(p)]
print("a=5, out=1 với mọi u:", any(cheat))
