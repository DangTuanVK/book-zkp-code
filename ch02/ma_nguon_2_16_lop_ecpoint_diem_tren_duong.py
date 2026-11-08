# Mã nguồn 2.16 - Lớp ECPoint: điểm trên đường cong Elliptic
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 80
# Trích tự động từ chapters/ch2/main.tex (dòng 2593) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.14 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_14_lop_fp_hoan_chinh_truong import *  # noqa
# --- Hết phần thêm ---

# === lab2_ec.py – Lớp ECPoint ===
class ECPoint:
    """Điểm trên đường cong y^2 = x^3 + ax + b (mod p)."""
    def __init__(self, x, y, curve):
        self.x, self.y, self.curve = x, y, curve
        if x is not None:
            assert y*y == x*x*x + curve.a*x + curve.b

    @property
    def is_infinity(self): return self.x is None

    def __add__(self, other):
        if self.is_infinity: return other
        if other.is_infinity: return self
        if self.x == other.x and self.y == -other.y:
            return self.curve.O
        if self == other:  # Nhân đôi
            lam = (Fp(3,self.curve.p)*self.x**2 + self.curve.a) \
                  / (Fp(2,self.curve.p)*self.y)
        else:
            lam = (other.y - self.y) / (other.x - self.x)
        x3 = lam**2 - self.x - other.x
        y3 = lam*(self.x - x3) - self.y
        return ECPoint(x3, y3, self.curve)

    def __neg__(self):
        return self if self.is_infinity else ECPoint(self.x,-self.y,self.curve)

    def __mul__(self, k):
        """Double-and-add: [k]P."""
        result, current = self.curve.O, self
        while k > 0:
            if k & 1: result = result + current
            current = current + current
            k >>= 1
        return result
    __rmul__ = __mul__

    def __eq__(self, o):
        if self.is_infinity and o.is_infinity: return True
        if self.is_infinity or o.is_infinity: return False
        return self.x == o.x and self.y == o.y

    def __repr__(self):
        return "O" if self.is_infinity else f"({self.x}, {self.y})"
