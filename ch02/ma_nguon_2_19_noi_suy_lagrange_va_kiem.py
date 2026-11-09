# Mã nguồn 2.19 - Nội suy Lagrange và kiểm tra Schwartz-Zippel trên F_p
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 87
# Trích tự động từ chapters/ch2/main.tex (dòng 2964) bằng extract.py; không sửa tay file này.

# === lab2_polynomial.py – Đa thức trên F_p ===
import random

p = 97  # Số nguyên tố đủ lớn để demo

def lagrange_interpolate(points, x_eval, p):
    """Tính f(x_eval) từ các điểm [(x0,y0), ...] trên F_p."""
    total = 0
    n = len(points)
    for i in range(n):
        xi, yi = points[i]
        num, den = 1, 1
        for j in range(n):
            if i != j:
                xj = points[j][0]
                num = (num * (x_eval - xj)) % p
                den = (den * (xi - xj)) % p
        total = (total + yi * num * pow(den, p - 2, p)) % p
    return total

# Tạo đa thức bí mật: f(x) = 3x^2 + 7x + 2 (mod 97)
def f_secret(x):
    return (3 * x**2 + 7 * x + 2) % p

# Tạo 3 điểm (cần d+1 = 3 điểm cho đa thức bậc 2)
points = [(1, f_secret(1)), (2, f_secret(2)), (3, f_secret(3))]
print(f"Điểm đã biết: {points}")

# Nội suy và kiểm tra tại điểm mới
for x_test in [0, 4, 5, 50]:
    y_interp = lagrange_interpolate(points, x_test, p)
    y_actual = f_secret(x_test)
    print(f"  f({x_test}) = {y_interp} (nội suy), "
          f"{y_actual} (thực), match: {y_interp == y_actual}")

# === Schwartz-Zippel: kiểm tra 2 đa thức bằng nhau ===
def g_secret(x):  # Đa thức khác
    return (3 * x**2 + 7 * x + 5) % p  # Khác f ở hệ số tự do

z = random.randint(0, p - 1)  # Điểm kiểm tra ngẫu nhiên (challenge)
print(f"\n--- Schwartz-Zippel Test ---")
print(f"z = {z}")
print(f"f(z) = {f_secret(z)}, g(z) = {g_secret(z)}")
print(f"f(z) == g(z)? {f_secret(z) == g_secret(z)}")
print(f"→ Nếu f ≠ g: f(z) = g(z) chỉ với xác suất ≤ d/p")
