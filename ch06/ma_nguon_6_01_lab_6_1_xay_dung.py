# Mã nguồn 6.1 - Lab 6.1: Xây dựng PLONKish gate table và kiểm tra constraints
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 6, trang 271
# Trích tự động từ chapters/ch6/main.tex (dòng 881) bằng extract.py; không sửa tay file này.

# === lab6_plonk.py – Mini PLONKish ===
# Bài toán: chứng minh biết x sao cho x^2 + x = 12
# (đáp án: x = 3 trên F_41, vì 9 + 3 = 12)

import random

p = 41
def mod(a): return a % p
def inv(a): return pow(a, p - 2, p)

# ============================================================
# BƯỚC 1: PLONKish Gate Table
# ============================================================
# Mỗi hàng: (a, b, c, qL, qR, qO, qM, qC)
# Constraint: qL*a + qR*b + qO*c + qM*(a*b) + qC = 0

# Gate 1: w1 = x * x (nhân)
#   qM=1, qO=-1: a*b - c = 0 → c = a*b
# Gate 2: out = w1 + x (cộng)
#   qL=1, qR=1, qO=-1: a + b - c = 0 → c = a+b
# Gate 3: out = 12 (hằng số)
#   qL=1, qC=-12: a - 12 = 0 → a = 12

# Selector table (cố định, public)
selectors = [
    # qL  qR  qO  qM  qC
    [  0,  0, -1,  1,  0],  # Gate 1: c = a * b
    [  1,  1, -1,  0,  0],  # Gate 2: c = a + b
    [  1,  0,  0,  0, -12], # Gate 3: a = 12
]

print("=== PLONKish Gate Table ===")
print(f"{'Gate':>5} {'qL':>4} {'qR':>4} {'qO':>4} {'qM':>4} {'qC':>4}")
for i, s in enumerate(selectors):
    print(f"{i+1:>5} {s[0]:>4} {s[1]:>4} {s[2]:>4} {s[3]:>4} {s[4]:>4}")

# ============================================================
# BƯỚC 2: Witness (wire assignment)
# ============================================================
x = 3  # Secret witness
w1 = mod(x * x)     # 9
out = mod(w1 + x)    # 12

# Wire table: mỗi hàng (a_i, b_i, c_i)
wires = [
    [x, x, w1],      # Gate 1: a=x, b=x, c=x^2
    [w1, x, out],     # Gate 2: a=x^2, b=x, c=x^2+x
    [out, 0, 0],      # Gate 3: a=out (kiểm tra = 12)
]

print(f"\n=== Wire Assignment (x={x}) ===")
print(f"{'Gate':>5} {'a':>5} {'b':>5} {'c':>5}")
for i, w in enumerate(wires):
    print(f"{i+1:>5} {w[0]:>5} {w[1]:>5} {w[2]:>5}")

# ============================================================
# BƯỚC 3: Kiểm tra Gate Constraints
# ============================================================
print(f"\n=== Gate Constraint Check ===")
all_ok = True
for i in range(len(selectors)):
    a, b, c = wires[i]
    qL, qR, qO, qM, qC = selectors[i]
    result = mod(qL*a + qR*b + qO*c + qM*(a*b) + qC)
    ok = result == 0
    print(f"  Gate {i+1}: {qL}*{a} + {qR}*{b} + {qO}*{c} "
          f"+ {qM}*{a}*{b} + {qC} = {result} → "
          f"{'OK' if ok else 'FAIL'}")
    all_ok &= ok
print(f"  All gates: {'PASS' if all_ok else 'FAIL'}")
