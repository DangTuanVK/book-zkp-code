# Mã nguồn 2.14 - Lớp Fp hoàn chỉnh: trường hữu hạn F_p
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 81
# Trích tự động từ chapters/ch2/main.tex (dòng 2610) bằng extract.py; không sửa tay file này.

# === lab2_field.py – Trường hữu hạn F_p hoàn chỉnh ===
class Fp:
    """Phần tử của trường hữu hạn F_p."""
    def __init__(self, val, p):
        self.val = val % p; self.p = p
    def _coerce(self, o):
        return Fp(o, self.p) if isinstance(o, int) else o
    def __add__(self, o): o=self._coerce(o); return Fp((self.val+o.val)%self.p, self.p)
    def __sub__(self, o): o=self._coerce(o); return Fp((self.val-o.val)%self.p, self.p)
    def __mul__(self, o): o=self._coerce(o); return Fp((self.val*o.val)%self.p, self.p)
    def __pow__(self, e): return Fp(pow(self.val, e, self.p), self.p)
    def __neg__(self):    return Fp(-self.val, self.p)
    def inv(self):        assert self.val!=0; return self**(self.p-2)
    def __truediv__(self, o): return self * self._coerce(o).inv()
    def __eq__(self, o):
        if isinstance(o, int): return self.val == o % self.p
        return self.val == o.val and self.p == o.p
    def __repr__(self):   return f"{self.val}"
    def __hash__(self):   return hash((self.val, self.p))
    __radd__ = __add__; __rmul__ = __mul__
    __rsub__ = lambda self, o: Fp(o, self.p) - self
