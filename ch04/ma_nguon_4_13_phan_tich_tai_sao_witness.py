# Mã nguồn 4.13 - Phân tích tại sao witness sai bị phát hiện qua đa thức
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 189
# Trích tự động từ chapters/ch4/main.tex (dòng 4228) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 4.12 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_4_12_mini_snark_prover_chi_dung import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 6: Phân tích – Tại sao witness sai bị phát hiện?
# ============================================================
print(f"\n=== Phân tích đa thức ===")
for name, poly in (("đúng, x=3", P), ("SAI, x=4", P_fake)):
    vals = [poly_eval(poly, r) for r in eval_domain]
    print(f"Witness {name}: P(r_i) tại H = {eval_domain}: {vals}")
# Witness sai chỉ vi phạm RC3: P(1) = P(2) = 0 nhưng P(3) ≠ 0.
# Chỉ cần TỒN TẠI một i với P(r_i) ≠ 0 là P không chia hết cho Z_H.

n = n_constraints
print(f"\nKẾT LUẬN:")
print(f"  Witness đúng: P(r_i) = 0 với mọi i -> Z_H | P -> có h(x)")
print(f"  Witness sai:  có i với P(r_i) != 0 -> P không chia hết")
print(f"                cho Z_H -> không tồn tại h(x)")
print(f"  deg P <= 2n - 2 = {2 * n - 2}: với h cố định trước, τ đều trong")
bound = f"{2 * n - 2}/{p - 4}"
print(f"  {{4, ..., {p - 1}}} bỏ sót gian lận với xác suất <= {bound}")
