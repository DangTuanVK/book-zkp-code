# Mã nguồn 5.9 - Lab 5.5: FRI verify - kiểm tra consistency và phát hiện witness sai
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 237
# Trích tự động từ chapters/ch5/main.tex (dòng 3171) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.8 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_08_lab_5_4_fri_folding import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 5: FRI Verify – Kiểm tra consistency
# ============================================================

print(f"\n=== FRI Query Phase ===")

# Verifier chọn q điểm ngẫu nhiên để kiểm tra
n_queries = 3
query_indices = random.sample(
    range(0, len(fri_layers[0][0]) // 2),
    min(n_queries, len(fri_layers[0][0]) // 2)
)

print(f"  Query indices: {query_indices}")

all_consistent = True
for qi in query_indices:
    print(f"\n  --- Query index {qi} ---")
    idx = qi

    for round_idx in range(len(alphas)):
        layer_evals = fri_layers[round_idx][0]
        next_evals = fri_layers[round_idx + 1][0]
        alpha = alphas[round_idx]

        # Lấy cặp giá trị
        idx_pair = idx * 2
        if idx_pair + 1 < len(layer_evals):
            f_left = layer_evals[idx_pair]
            f_right = layer_evals[idx_pair + 1]
            f_next = next_evals[idx] if idx < len(next_evals) else None

            # Kiểm tra consistency (đơn giản hóa)
            f_combined = mod(f_left + alpha * f_right)
            consistent = (f_next is not None)

            print(f"    Round {round_idx+1}: f[{idx_pair}]={f_left}, "
                  f"f[{idx_pair+1}]={f_right}, "
                  f"alpha={alpha}, next={f_next}")

        idx = idx // 2

print(f"\n  FRI Verify: completed {n_queries} queries")

# ============================================================
# BƯỚC 6: So sánh – witness đúng vs sai
# ============================================================
print(f"\n=== So sánh: Witness đúng vs sai ===")

# Trace sai: a=3 nhưng bước 2 sai
bad_trace = [3, 9, 80, 62]  # 80 ≠ 81 = 9^2
print(f"Bad trace: {bad_trace}")
print(f"Transition check:")
for i in range(len(bad_trace) - 1):
    expected = mod(bad_trace[i] ** 2)
    actual = bad_trace[i + 1]
    ok = expected == actual
    print(f"  T[{i+1}] = T[{i}]^2? {actual} vs {expected} → "
          f"{'OK' if ok else 'FAIL'}")
print(f"→ AIR constraint vi phạm → đa thức constraint C(x) ≠ 0")
print(f"→ FRI sẽ phát hiện: C(x)/Z_H(x) không phải đa thức bậc thấp")
