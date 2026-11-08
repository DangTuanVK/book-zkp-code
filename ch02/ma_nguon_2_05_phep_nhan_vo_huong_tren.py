# Mã nguồn 2.5 - Phép nhân vô hướng trên đường cong Elliptic (double-and-add)
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 53
# Trích tự động từ chapters/ch2/main.tex (dòng 827) bằng extract.py; không sửa tay file này.

def scalar_mult(k, P, a, p):
    """Tính [k]P trên đường cong y^2 = x^3 + ax + b (mod p).
    Thuật toán double-and-add: O(log k) phép cộng điểm."""
    if k == 0:
        return None  # Điểm vô cực O
    result = None  # O (phần tử đơn vị)
    current = P
    while k > 0:
        if k & 1:  # bit thấp nhất = 1
            result = point_add(result, current, a, p)
        current = point_add(current, current, a, p)  # double
        k >>= 1
    return result
