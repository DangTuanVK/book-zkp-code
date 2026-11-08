# Mã nguồn 2.13 - Demo Merkle proof: chứng minh phần tử thuộc cây 8 lá và cây 5 lá
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 79
# Trích tự động từ chapters/ch2/main.tex (dòng 2460) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.12 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_12_tao_va_xac_minh_merkle import *  # noqa
# --- Hết phần thêm ---

# === Demo: chứng minh item_3 thuộc cây 8 lá ===
data = [f"item_{i}".encode() for i in range(8)]
leaves = [sha256(d) for d in data]
tree = build_merkle_tree(leaves)
root = tree[-1][0]

index = 3
proof = get_merkle_proof(tree, index)
valid = verify_merkle_proof(leaves[index], proof, root)
print(f"Root: {root.hex()[:16]}...")
print(f"Proof cho item_{index}: {len(proof)} sibling hashes")
print(f"Kết quả xác minh: {valid}")  # True

# === Số lá lẻ: cây 5 lá, kiểm tra mọi lá (kể cả lá cuối) ===
leaves5 = [sha256(f"item_{i}".encode()) for i in range(5)]
tree5 = build_merkle_tree(leaves5)
root5 = tree5[-1][0]
ok = [verify_merkle_proof(leaves5[i], get_merkle_proof(tree5, i), root5)
      for i in range(5)]
print(f"Cây 5 lá, xác minh từng lá: {ok}")  # 5 lần True
