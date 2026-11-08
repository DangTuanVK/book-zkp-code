# Mã nguồn 13.1 - Folding hai và ba instance relaxed R1CS theo công thức của Nova
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 13, trang 418
# Trích tự động từ chapters/ch13/main.tex (dòng 171) bằng extract.py; không sửa tay file này.

# === nova_fold.py – Folding relaxed R1CS (không có commitment) ===
import random

p = 97                          # trường nhỏ để dễ theo dõi
rng = random.Random(2026)       # cố định hạt giống: kết quả tái lập được

# Circuit: y = x^2 + x.  Vector z = [u, y, x, w]  (u thay cho hằng 1)
#   RC1: x * x = w        RC2: (w + x) * u = y
A = [[0, 0, 1, 0], [0, 0, 1, 1]]
B = [[0, 0, 1, 0], [1, 0, 0, 0]]
C = [[0, 0, 0, 1], [0, 1, 0, 0]]

def mat_vec(M, z):
    return [sum(m * v for m, v in zip(row, z)) % p for row in M]

def hadamard(a, b):
    return [(x * y) % p for x, y in zip(a, b)]

def is_relaxed_sat(z, E):
    # Kiểm tra (Az) * (Bz) = u·(Cz) + E (nhân từng phần tử), với u = z[0]
    u = z[0]
    lhs = hadamard(mat_vec(A, z), mat_vec(B, z))
    rhs = [(u * c + e) % p for c, e in zip(mat_vec(C, z), E)]
    return lhs == rhs

def fresh(x):
    # Instance R1CS thông thường: u = 1, E = 0
    w = x * x % p
    return [1, (w + x) % p, x, w], [0, 0]

def fold(z1, E1, z2, E2, r):
    u1, u2 = z1[0], z2[0]
    Az1, Bz1, Cz1 = mat_vec(A, z1), mat_vec(B, z1), mat_vec(C, z1)
    Az2, Bz2, Cz2 = mat_vec(A, z2), mat_vec(B, z2), mat_vec(C, z2)
    # Cross term T = Az1*Bz2 + Az2*Bz1 − u1·Cz2 − u2·Cz1 (nhân từng phần tử)
    T = [(a1 * b2 + a2 * b1 - u1 * c2 - u2 * c1) % p
         for a1, b1, c1, a2, b2, c2 in zip(Az1, Bz1, Cz1, Az2, Bz2, Cz2)]
    z = [(a + r * b) % p for a, b in zip(z1, z2)]   # gồm u = u1 + r·u2
    E = [(e1 + r * t + r * r * e2) % p for e1, t, e2 in zip(E1, T, E2)]
    return z, E, T

z1, E1 = fresh(3)               # 3^2 + 3 = 12
z2, E2 = fresh(5)               # 5^2 + 5 = 30
print("z1 =", z1, " thỏa:", is_relaxed_sat(z1, E1))
print("z2 =", z2, " thỏa:", is_relaxed_sat(z2, E2))

# Gộp "ngây thơ": cộng tuyến tính, bỏ qua T và E
r = rng.randrange(1, p)
z_naive = [(a + r * b) % p for a, b in zip(z1, z2)]
print(f"\nr = {r}")
print("Gộp ngây thơ  z =", z_naive, " thỏa:", is_relaxed_sat(z_naive, [0, 0]))

# Folding của Nova
z, E, T = fold(z1, E1, z2, E2, r)
print("Cross term    T =", T)
print("Folded        z =", z, " E =", E, " thỏa:", is_relaxed_sat(z, E))

# Gộp tiếp instance thứ ba (giống một bước IVC)
z3, E3 = fresh(7)               # 7^2 + 7 = 56
r2 = rng.randrange(1, p)
z, E, T = fold(z, E, z3, E3, r2)
print(f"\nr = {r2}")
print("Folded lần 2  z =", z, " E =", E, " thỏa:", is_relaxed_sat(z, E))
