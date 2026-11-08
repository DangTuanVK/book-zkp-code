# Mã nguồn 4.4 - Đếm số ràng buộc của ba cặp cách biên dịch: thẳng và tối ưu
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 138
# Trích tự động từ chapters/ch4/main.tex (dòng 1213) bằng extract.py; không sửa tay file này.

# Đếm số ràng buộc nhân (R1CS) của ba cặp cách biên dịch: thẳng và tối ưu
p = 2**61 - 1                       # một số nguyên tố Mersenne làm trường mẫu

class CS:
    """Hệ ràng buộc tối giản: chỉ đếm phép nhân hai biến (mỗi phép = 1 ràng buộc)."""
    def __init__(self):
        self.n = 0
    def mul(self, a, b):
        self.n += 1
        return a * b % p
    def check_mul(self, a, b, c):   # ràng buộc a * b = c
        self.n += 1
        assert a * b % p == c % p

# 1) Nghịch đảo: tính b^(p-2) trong circuit, hay nhận gợi ý và kiểm tra
def inv_direct(cs, b):
    r, e, base = 1, p - 2, b
    while e:
        if e & 1:
            r = cs.mul(r, base)
        base = cs.mul(base, base)
        e >>= 1
    return r

def inv_hint(cs, b):
    u = pow(b, p - 2, p)            # tính NGOÀI circuit (miễn phí)
    cs.check_mul(b, u, 1)           # trong circuit chỉ kiểm tra b * u = 1
    return u

# 2) Kiểm tra x < 2^k: phân rã k bit, hay biểu diễn theo limb 16 bit
def range_bits(cs, x, k):
    bits = [(x >> i) & 1 for i in range(k)]
    for b in bits:
        cs.check_mul(b, 1 - b, 0)   # b(1-b) = 0: mỗi bit một ràng buộc
    assert sum(b << i for i, b in enumerate(bits)) == x  # tổ hợp tuyến tính: miễn phí
def range_lookup(cs, x, k, w=16):
    limbs = [(x >> (w * i)) & (2**w - 1) for i in range(k // w)]
    cs.n += len(limbs)              # mỗi limb một lần tra bảng {0..2^w-1}
    assert sum(l << (w * i) for i, l in enumerate(limbs)) == x

# 3) Đọc mảng tại chỉ số bí mật: bộ chọn one-hot, hay kiểm tra bộ nhớ
def read_mux(cs, arr, idx):
    sel = [1 if i == idx else 0 for i in range(len(arr))]
    for s in sel:
        cs.check_mul(s, 1 - s, 0)   # s là bit
    assert sum(sel) == 1            # đúng một bit bằng 1: tuyến tính
    return sum(cs.mul(s, a) for s, a in zip(sel, arr)) % p
def read_memcheck(cs, arr, idx):
    cs.n += 2                       # khấu hao: vài ràng buộc cho mỗi lần đọc
    return arr[idx]                 # (chi phí hoán vị/lookup chia đều cho các lần đọc)

def cost(f, *args):
    cs = CS(); f(cs, *args); return cs.n

arr = list(range(100, 1124))        # mảng 1024 phần tử
print(f"{'Phép toán':<28}{'Thẳng':>8}{'Tối ưu':>8}")
print(f"{'Nghịch đảo trong F_p':<28}{cost(inv_direct, 12345):>8}{cost(inv_hint, 12345):>8}")
print(f"{'Kiểm tra x < 2^64':<28}{cost(range_bits, 2**60 + 7, 64):>8}"
      f"{cost(range_lookup, 2**60 + 7, 64):>8}")
print(f"{'Đọc arr[idx], n = 1024':<28}{cost(read_mux, arr, 777):>8}"
      f"{cost(read_memcheck, arr, 777):>8}")
