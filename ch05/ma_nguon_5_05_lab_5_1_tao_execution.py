# Mã nguồn 5.5 - Lab 5.1: Tạo execution trace và kiểm tra AIR constraints
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 246
# Trích tự động từ chapters/ch5/main.tex (dòng 3051) bằng extract.py; không sửa tay file này.

# === lab5_fri.py – Mini-FRI Protocol trên F_97 ===
import hashlib

p = 97  # Trường F_97
def mod(a): return a % p
def inv(a): return pow(a % p, p - 2, p)

# ============================================================
# BƯỚC 1: Execution Trace cho a^8 (bình phương liên tiếp)
# ============================================================
a_input = 3
trace = [a_input]
for _ in range(3):
    trace.append(mod(trace[-1] ** 2))

print(f"=== Execution Trace (a^8, a={a_input}) ===")
print(f"  trace = {trace}, kết quả {a_input}^8 = {trace[-1]} (mod {p})")

# Kiểm tra AIR transition: T[i+1] = T[i]^2
def check_air(tr):
    ok_all = True
    for i in range(len(tr) - 1):
        ok = tr[i + 1] == mod(tr[i] ** 2)
        print(f"  T[{i+1}] = T[{i}]^2? {tr[i+1]} vs {mod(tr[i]**2)}"
              f" -> {'OK' if ok else 'FAIL'}")
        ok_all &= ok
    return ok_all

print("AIR transition constraints:")
print(f"  Tất cả: {'PASS' if check_air(trace) else 'FAIL'}")
