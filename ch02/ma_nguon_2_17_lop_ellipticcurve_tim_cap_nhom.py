# Mã nguồn 2.17 - Lớp EllipticCurve, tìm cấp nhóm và minh họa ECDLP
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 83
# Trích tự động từ chapters/ch2/main.tex (dòng 2793) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.16 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_16_lop_ecpoint_diem_tren_duong import *  # noqa
# --- Hết phần thêm ---

# === Lớp EllipticCurve và demo ===
class EllipticCurve:
    """Đường cong y^2 = x^3 + ax + b trên F_p."""
    def __init__(self, a, b, p):
        self.a, self.b, self.p = Fp(a,p), Fp(b,p), p
        self.O = ECPoint(None, None, self)
    def point(self, x, y):
        return ECPoint(Fp(x,self.p), Fp(y,self.p), self)

E = EllipticCurve(a=1, b=1, p=23)
G = E.point(0, 1)
print(f"Generator G = {G}")

# Tìm bậc nhóm
for k in range(1, 50):
    kG = k * G
    if kG.is_infinity:
        print(f"Bậc nhóm: [{k}]G = O → order = {k}")
        order = k; break
    print(f"  [{k:2d}]G = {kG}")

# ECDLP demo
import random
x_secret = random.randint(1, order - 1)
Q = x_secret * G
print(f"Secret x={x_secret}, Public Q={Q}")
print(f"Với p~2^256: tìm x từ Q KHÔNG KHẢ THI!")
