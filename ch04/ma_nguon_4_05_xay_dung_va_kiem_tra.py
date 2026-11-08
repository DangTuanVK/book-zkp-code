# Mã nguồn 4.5 - Xây dựng và kiểm tra hệ ràng buộc R1CS
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 145
# Trích tự động từ chapters/ch4/main.tex (dòng 1657) bằng extract.py; không sửa tay file này.

# === R1CS cho x^3 + x + 5 = 35 ===
import numpy as np

p = 41  # Trường F_41

# Véc-tơ biến: s = [1, out, x, w1, w2]
# Với x = 3: s = [1, 35, 3, 9, 27]

# Ma trận A, B, C (mỗi hàng = 1 ràng buộc)
#              1   out  x   w1  w2
A = np.array([[0,   0,  1,  0,  0],    # Constraint 1: x
              [0,   0,  0,  1,  0],    # Constraint 2: w1
              [-5,  1, -1,  0, -1]],   # Constraint 3: out-w2-x-5
             dtype=int)

B = np.array([[0,   0,  1,  0,  0],    # Constraint 1: x
              [0,   0,  1,  0,  0],    # Constraint 2: x
              [1,   0,  0,  0,  0]],   # Constraint 3: 1
             dtype=int)

C = np.array([[0,   0,  0,  1,  0],    # Constraint 1: w1
              [0,   0,  0,  0,  1],    # Constraint 2: w2
              [0,   0,  0,  0,  0]],   # Constraint 3: 0
             dtype=int)

def check_r1cs(A, B, C, s, p):
    """Kiểm tra (A·s) * (B·s) = C·s (mod p), nhân từng phần tử."""
    As = A.dot(s) % p
    Bs = B.dot(s) % p
    Cs = C.dot(s) % p
    lhs = (As * Bs) % p
    return np.array_equal(lhs, Cs)

# Witness đúng: x = 3
x = 3
s_valid = np.array([1, 35, x, x**2, x**3])
print(f"s = {s_valid}")
print(f"R1CS valid: {check_r1cs(A, B, C, s_valid, p)}")

# Witness sai: x = 4
x_bad = 4
s_bad = np.array([1, 35, x_bad, x_bad**2, x_bad**3])
print(f"\ns_bad = {s_bad}")
print(f"R1CS valid: {check_r1cs(A, B, C, s_bad, p)}")

# Chi tiết từng ràng buộc
print(f"\nChi tiết (x=3):")
s = s_valid
for i in range(len(A)):
    ai = A[i].dot(s) % p
    bi = B[i].dot(s) % p
    ci = C[i].dot(s) % p
    ok = (ai * bi) % p == ci
    print(f"  RC{i+1}: {ai} × {bi} = {(ai*bi)%p}, "
          f"expected {ci}, {'OK' if ok else 'FAIL'}")
