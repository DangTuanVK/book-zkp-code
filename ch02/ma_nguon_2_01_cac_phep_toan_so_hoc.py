# Mã nguồn 2.1 - Các phép toán số học modular cơ bản trong Python
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 42
# Trích tự động từ chapters/ch2/main.tex (dòng 176) bằng extract.py; không sửa tay file này.

# === Số học modular cơ bản ===
p = 7  # Modulus (số nguyên tố)

# Phép cộng, trừ, nhân
print(f"(5 + 4) mod {p} = {(5 + 4) % p}")       # 2
print(f"(3 - 5) mod {p} = {(3 - 5) % p}")       # 5
print(f"(4 * 5) mod {p} = {(4 * 5) % p}")       # 6

# Nghịch đảo modular: a^{-1} = a^{p-2} mod p (Fermat nhỏ)
a = 3
inv_a = pow(a, p - 2, p)  # pow(base, exp, mod) tính nhanh
print(f"{a}^(-1) mod {p} = {inv_a}")             # 5
print(f"Kiểm tra: {a} * {inv_a} mod {p} = {(a * inv_a) % p}")  # 1

# "Phép chia": a / b = a * b^{-1} mod p
def mod_div(a, b, p):
    """Phép chia modular: a / b mod p"""
    return (a * pow(b, p - 2, p)) % p

print(f"6 / 3 mod {p} = {mod_div(6, 3, p)}")    # 2
print(f"1 / 3 mod {p} = {mod_div(1, 3, p)}")    # 5

# Lũy thừa modular
g, x = 3, 100
y = pow(g, x, p)
print(f"{g}^{x} mod {p} = {y}")  # Tính nhanh dù x rất lớn
