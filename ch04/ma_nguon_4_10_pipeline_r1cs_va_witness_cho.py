# Mã nguồn 4.10 - Pipeline R1CS và witness cho Mini-SNARK
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 174
# Trích tự động từ chapters/ch4/main.tex (dòng 3926) bằng extract.py; không sửa tay file này.

# === lab4_minisnark.py – Mini-SNARK end-to-end ===
# Bài toán: chứng minh biết x sao cho x^3 + x + 5 = 35
# (đáp án: x = 3)

import random

p = 41  # Trường F_41 (nhỏ để dễ quan sát)

def mod(a, p=p): return a % p
def inv(a, p=p): return pow(a, p - 2, p)

# ============================================================
# BƯỚC 1: Xác định R1CS
# ============================================================
# Biến: s = [1, out, x, w1=x^2, w2=x^3]
# Ràng buộc:
#   RC1: x * x = w1
#   RC2: w1 * x = w2
#   RC3: (out - w2 - x - 5) * 1 = 0

#              1    out   x    w1   w2
A = [         [0,    0,   1,   0,   0],    # RC1: x
              [0,    0,   0,   1,   0],    # RC2: w1
              [p-5,  1,   p-1, 0,   p-1]]  # RC3: -5+out-x-w2

B = [         [0,    0,   1,   0,   0],    # RC1: x
              [0,    0,   1,   0,   0],    # RC2: x
              [1,    0,   0,   0,   0]]    # RC3: 1

C = [         [0,    0,   0,   1,   0],    # RC1: w1
              [0,    0,   0,   0,   1],    # RC2: w2
              [0,    0,   0,   0,   0]]    # RC3: 0

n_constraints = 3  # Số ràng buộc
n_vars = 5         # Số biến

# ============================================================
# BƯỚC 2: Witness (assignment)
# ============================================================
x_secret = 3
out_public = 35
w1 = mod(x_secret * x_secret)
w2 = mod(w1 * x_secret)
s = [1, out_public, x_secret, w1, w2]

print(f"=== BƯỚC 1-2: R1CS & Witness ===")
print(f"Witness s = {s}")

# Kiểm tra R1CS
for i in range(n_constraints):
    ai = sum(A[i][j] * s[j] for j in range(n_vars)) % p
    bi = sum(B[i][j] * s[j] for j in range(n_vars)) % p
    ci = sum(C[i][j] * s[j] for j in range(n_vars)) % p
    ok = (ai * bi) % p == ci
    print(f"  RC{i+1}: {ai} * {bi} = {(ai*bi)%p}, exp {ci}, {'OK' if ok else 'FAIL'}")
