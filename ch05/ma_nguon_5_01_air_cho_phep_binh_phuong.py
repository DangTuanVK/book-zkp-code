# Mã nguồn 5.1 - AIR cho phép bình phương liên tiếp trên F_97
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 206
# Trích tự động từ chapters/ch5/main.tex (dòng 811) bằng extract.py; không sửa tay file này.

# === AIR cho a^8 (bình phương liên tiếp) trên F_97 ===

p = 97

def mod(a): return a % p

# === Execution Trace ===
a = 3
trace = [a]
for _ in range(3):  # 3 bước bình phương: a -> a^2 -> a^4 -> a^8
    trace.append(mod(trace[-1] ** 2))

print(f"Execution trace (a^8, a={a}):")
for i, val in enumerate(trace):
    print(f"  Step {i}: {val}")
print(f"  Kết quả: {a}^8 = {trace[-1]} (mod {p})")

# === Transition constraint: x' = x^2 ===
print(f"\nKiểm tra transition constraints:")
for i in range(len(trace) - 1):
    x_curr = trace[i]
    x_next = trace[i + 1]
    residual = mod(x_next - x_curr ** 2)
    print(f"  Step {i}->{i+1}: {x_next} - {x_curr}^2 = "
          f"{x_next} - {mod(x_curr**2)} = {residual} "
          f"{'OK' if residual == 0 else 'FAIL'}")

# === Boundary constraints ===
print(f"\nBoundary constraints:")
print(f"  T[0] = {trace[0]} == {a}? {trace[0] == a}")
expected_output = mod(a ** 8)
print(f"  T[3] = {trace[3]} == {expected_output}? "
      f"{trace[3] == expected_output}")

# === Nội suy trace thành đa thức ===
# Domain: roots of unity (đơn giản hóa: dùng {0,1,2,3})
domain = list(range(len(trace)))

def lagrange_eval(values, domain, x):
    """Nội suy Lagrange tại x."""
    n = len(values)
    result = 0
    for i in range(n):
        num, den = 1, 1
        for j in range(n):
            if i != j:
                num = mod(num * (x - domain[j]))
                den = mod(den * (domain[i] - domain[j]))
        Li = mod(num * pow(den, p - 2, p))
        result = mod(result + values[i] * Li)
    return result

# Kiểm tra: t(domain[i]) == trace[i]
print(f"\nNội suy Lagrange:")
for i in range(len(trace)):
    val = lagrange_eval(trace, domain, domain[i])
    print(f"  t({domain[i]}) = {val} == {trace[i]}? {val == trace[i]}")

# Kiểm tra constraint trên đa thức tại điểm ngẫu nhiên
import random
tau = random.randint(10, p - 1)
t_tau = lagrange_eval(trace, domain, tau)
# "Shift": t(x+1) ≈ t_0(ωx) trong roots of unity version
t_tau_next = lagrange_eval(trace, domain, tau + 1)  # Đơn giản hóa
C_tau = mod(t_tau_next - t_tau ** 2)
print(f"\nConstraint polynomial C(τ={tau}):")
print(f"  t(τ) = {t_tau}, t(τ+1) = {t_tau_next}")
print(f"  C(τ) = t(τ+1) - t(τ)^2 = {C_tau}")
