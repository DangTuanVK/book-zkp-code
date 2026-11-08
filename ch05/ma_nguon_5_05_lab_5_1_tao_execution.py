# Mã nguồn 5.5 - Lab 5.1: Tạo execution trace và kiểm tra AIR constraints
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 232
# Trích tự động từ chapters/ch5/main.tex (dòng 2948) bằng extract.py; không sửa tay file này.

# === lab5_fri.py – Mini-FRI Protocol ===
import hashlib
import random

p = 97  # Trường F_97
def mod(a): return a % p
def inv(a): return pow(a, p - 2, p)

# ============================================================
# BƯỚC 1: Execution Trace cho a^8 (bình phương liên tiếp)
# ============================================================
a_input = 3
trace = [a_input]
for _ in range(3):
    trace.append(mod(trace[-1] ** 2))

print(f"=== Execution Trace (a^8, a={a_input}) ===")
for i, val in enumerate(trace):
    print(f"  T[{i}] = {val}")
print(f"  Kết quả: {a_input}^8 = {trace[-1]}")

# Kiểm tra AIR transition: T[i+1] = T[i]^2
print(f"\nAIR transition constraints:")
all_ok = True
for i in range(len(trace) - 1):
    ok = trace[i + 1] == mod(trace[i] ** 2)
    print(f"  T[{i+1}] = T[{i}]^2? {trace[i+1]} = {mod(trace[i]**2)}"
          f" → {'OK' if ok else 'FAIL'}")
    all_ok &= ok
print(f"  All constraints: {'PASS' if all_ok else 'FAIL'}")
