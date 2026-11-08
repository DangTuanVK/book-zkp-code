# Mã nguồn 2.8 - Nội suy Lagrange trên trường hữu hạn F_p
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 62
# Trích tự động từ chapters/ch2/main.tex (dòng 1495) bằng extract.py; không sửa tay file này.

# === Nội suy Lagrange trên F_p ===

def lagrange_interpolation(points, p):
    """Nội suy Lagrange: cho danh sách [(x0,y0), (x1,y1), ...],
    trả về hàm đa thức f(x) trên F_p."""
    def f(x):
        total = 0
        n = len(points)
        for i in range(n):
            xi, yi = points[i]
            # Tính L_i(x)
            numerator = 1
            denominator = 1
            for j in range(n):
                if j != i:
                    xj = points[j][0]
                    numerator = (numerator * (x - xj)) % p
                    denominator = (denominator * (xi - xj)) % p
            # L_i(x) = numerator / denominator
            Li = (numerator * pow(denominator, p - 2, p)) % p
            total = (total + yi * Li) % p
        return total
    return f

# Ví dụ: tìm đa thức bậc 2 qua 3 điểm trên F_17
p = 17
points = [(1, 3), (2, 7), (4, 5)]
f = lagrange_interpolation(points, p)

# Kiểm tra: f(x) đi qua tất cả các điểm
for x, y in points:
    print(f"f({x}) = {f(x)}, expected {y}, match: {f(x) == y}")

# Tính f tại điểm mới
print(f"f(3) = {f(3)}")  # Giá trị tại x=3
print(f"f(0) = {f(0)}")  # Hệ số tự do a_0
