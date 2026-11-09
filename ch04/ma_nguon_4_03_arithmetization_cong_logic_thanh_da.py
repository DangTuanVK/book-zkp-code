# Mã nguồn 4.3 - Arithmetization: cổng logic thành đa thức trên F_p, và chi phí của một bộ cộng 8 bit so với phép cộng bản địa
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 131
# Trích tự động từ chapters/ch4/main.tex (dòng 878) bằng extract.py; không sửa tay file này.

# === Từ cổng logic đến cổng số học: mọi mạch Boolean "dịch" được sang F_p ===
p = 2**61 - 1                              # một số nguyên tố bất kỳ đủ lớn
muls = 0                                   # đếm số cổng nhân (chi phí trong R1CS)

def mul(a, b):
    global muls
    muls += 1
    return a * b % p

NOT = lambda a: (1 - a) % p                # 1 - a
AND = lambda a, b: mul(a, b)               # a * b
OR  = lambda a, b: (a + b - mul(a, b)) % p # a + b - a b
XOR = lambda a, b: (a + b - 2 * mul(a, b)) % p

# 1) Kiểm tra bảng chân trị: đa thức trùng với phép logic trên {0, 1}
for a in (0, 1):
    for b in (0, 1):
        assert (NOT(a), AND(a, b), OR(a, b), XOR(a, b)) == \
               (1 - a, a & b, a | b, a ^ b)
print("Bảng chân trị NOT/AND/OR/XOR: khớp trên {0,1}")

# 2) Bộ cộng 8 bit (ripple-carry) xây hoàn toàn bằng cổng số học
def add8(x_bits, y_bits):
    out, carry = [], 0
    for a, b in zip(x_bits, y_bits):       # bit thấp trước
        s = XOR(a, b)
        out.append(XOR(s, carry))
        carry = OR(AND(a, b), AND(s, carry))
    return out

to_bits = lambda v: [(v >> i) & 1 for i in range(8)]
from_bits = lambda bs: sum(b << i for i, b in enumerate(bs))

muls = 0
x, y = 200, 99
z = from_bits(add8(to_bits(x), to_bits(y)))
print(f"add8({x}, {y}) = {z}  (đúng: {(x + y) % 256}), dùng {muls} cổng nhân")

# 3) So sánh: phép cộng gốc trên F_p không tốn cổng nhân nào
muls = 0
z_native = (x + y) % p
print(f"Cộng trực tiếp trên F_p: {z_native}, dùng {muls} cổng nhân")
