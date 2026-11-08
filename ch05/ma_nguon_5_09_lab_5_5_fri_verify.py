# Mã nguồn 5.9 - Lab 5.5: FRI verify - kiểm tra tính nhất quán giữa các tầng và phát hiện witness sai
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 251
# Trích tự động từ chapters/ch5/main.tex (dòng 3282) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.8 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_08_lab_5_4_fri_folding import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 5: FRI Verify – Query phase
# ============================================================
def fri_verify(layers, n_queries=3, verbose=True):
    """Verifier chỉ đọc vài giá trị (kèm đường Merkle) ở mỗi tầng."""
    roots = [root for _, _, (root, _) in layers]
    betas = [challenge("fri", rt) for rt in roots[:-1]]  # tự tính lại beta
    final = layers[-1][0]
    if len(set(final)) != 1:                          # tầng cuối phải hằng số
        return "từ chối: tầng cuối không phải hằng số"
    N0 = len(layers[0][0])
    for qi in range(n_queries):
        j = challenge(*roots, "query", qi) % (N0 // 2)  # vị trí do băm chọn
        for r in range(len(betas)):
            vals, xs, (root, tree) = layers[r]
            h = len(vals) // 2
            a, b = j % h, j % h + h                    # cặp (x, -x)
            for i in (a, b):              # Prover mở kèm đường Merkle
                if not verify_proof(root, i, vals[i], get_proof(tree, i)):
                    return f"từ chối: Merkle sai ở tầng {r}"
            u = mod((vals[a] + vals[b]) * inv(2)
                    + betas[r] * (vals[a] - vals[b]) * inv(2 * xs[a]))
            nxt = layers[r + 1][0][a]                  # giá trị đã cam kết
            if verbose:
                print(f"    query {qi} (j={j}), vòng {r+1}: gấp f[{a}]={vals[a]}, "
                      f"f[{b}]={vals[b]} -> {u}, tầng sau [{a}] = {nxt}")
            if u != nxt:
                return f"từ chối: vòng gấp {r+1} không nhất quán"
            j = a
    return "chấp nhận"

print("\n=== FRI Query Phase ===")
print("[1] Prover trung thực:")
print(f"  -> {fri_verify(fri_layers)}")

# Prover gian lận: gửi tầng 1 bị sửa (cộng 1 vào mọi giá trị) và cam kết nó
vals1, xs1, _ = fri_layers[1]
bad1 = [mod(v + 1) for v in vals1]
tree1 = build_merkle(bad1)
v2, x2 = fri_fold(bad1, xs1, challenge("fri", tree1[0]))   # gấp tiếp từ tầng giả
tampered = [fri_layers[0], (bad1, xs1, tree1), (v2, x2, build_merkle(v2))]
print("[2] Tầng 1 bị sửa:")
print(f"  -> {fri_verify(tampered)}")

# ============================================================
# BƯỚC 6: Witness đúng vs sai – FRI trên thương ràng buộc
# ============================================================
def quotient_on_L(tr):
    """Q(x) = (t(omega x) - t(x)^2) / Z_tr(x) trên L, Z_tr = (x^4-1)/(x - omega^3)."""
    tl = [lagrange_eval(tr, H, x) for x in L]
    return [mod((tl[(j + 4) % N] - tl[j] ** 2) * (L[j] - H[-1])
                * inv(pow(L[j], n, p) - 1)) for j in range(N)]

print("\n=== Witness đúng vs sai ===")
bad_trace = [3, 9, 80, 62]                            # 80 khác 81 = 9^2
for name, tr in (("Trace đúng", trace), ("Trace sai ", bad_trace)):
    lay, _ = fri_commit(quotient_on_L(tr), L, rounds=2)
    print(f"  {name} {tr}: tầng cuối = {lay[-1][0]}")
    print(f"    -> {fri_verify(lay, verbose=False)}")
