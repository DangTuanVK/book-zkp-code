# Mã nguồn 2.3 - Lớp Fp biểu diễn phần tử trường hữu hạn F_p
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 48
# Trích tự động từ chapters/ch2/main.tex (dòng 537) bằng extract.py; không sửa tay file này.

# === Trường hữu hạn F_p đơn giản ===
class Fp:
    """Phần tử của trường hữu hạn F_p."""
    def __init__(self, val, p):
        self.val = val % p
        self.p = p

    def __add__(self, other):  return Fp(self.val + other.val, self.p)
    def __sub__(self, other):  return Fp(self.val - other.val, self.p)
    def __mul__(self, other):  return Fp(self.val * other.val, self.p)
    def __neg__(self):         return Fp(-self.val, self.p)
    def inv(self):             return Fp(pow(self.val, self.p - 2, self.p), self.p)
    def __truediv__(self, other): return self * other.inv()
    def __eq__(self, other):   return self.val == other.val and self.p == other.p
    def __repr__(self):        return f"{self.val}"

# Ví dụ: F_7
p = 7
a, b = Fp(5, p), Fp(4, p)

print(f"a + b = {a + b}")     # 2
print(f"a - b = {a - b}")     # 1
print(f"a * b = {a * b}")     # 6
print(f"a / b = {a / b}")     # 5 * 4^{-1} = 5 * 2 = 10 mod 7 = 3

# Kiểm tra tính chất trường: a * a^{-1} = 1
print(f"a * a^(-1) = {a * a.inv()}")  # 1
