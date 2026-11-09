# Mã nguồn 2.18b - (phần nối tiếp của Mã nguồn 2.18)
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 85
# Trích tự động từ chapters/ch2/main.tex (dòng 2879) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.18 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_18_pedersen_commitment_cam_ket_va import *  # noqa
# --- Hết phần thêm ---

# === Tính chất homomorphic (cộng được) ===
# C(v1, r1) + C(v2, r2) = C(v1+v2, r1+r2)
v1, r1 = 3, random.randrange(order)
v2, r2 = 7, random.randrange(order)

C1 = commit(v1, r1)
C2 = commit(v2, r2)
C_sum = C1 + C2
C_direct = commit((v1 + v2) % order, (r1 + r2) % order)

print(f"\n--- Pedersen Homomorphic ---")
print(f"C({v1}) + C({v2}) = {C_sum}")
print(f"C({v1}+{v2}={v1+v2}) = {C_direct}")
print(f"Bằng nhau? {C_sum == C_direct}")  # True
print(f"→ Có thể cộng commitment mà không cần mở")
