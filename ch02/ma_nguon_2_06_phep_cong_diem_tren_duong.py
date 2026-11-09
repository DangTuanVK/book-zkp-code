# Mã nguồn 2.6 - Phép cộng điểm trên đường cong Elliptic F_p
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 58
# Trích tự động từ chapters/ch2/main.tex (dòng 1121) bằng extract.py; không sửa tay file này.

# === Phép cộng điểm trên đường cong Elliptic ===
def point_add(P, Q, a, p):
    """Cộng hai điểm P, Q trên y^2 = x^3 + ax + b (mod p).
    None đại diện cho điểm vô cực O."""
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None  # P + (-P) = O
    if P == Q:  # Nhân đôi (tangent)
        lam = (3 * x1**2 + a) * pow(2 * y1, p - 2, p) % p
    else:       # Cộng hai điểm khác nhau (secant)
        lam = (y2 - y1) * pow(x2 - x1, p - 2, p) % p
    x3 = (lam**2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)
