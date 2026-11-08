# Mã nguồn 5.7 - Lab 5.3: Xây dựng Merkle tree để commit các evaluation
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 234
# Trích tự động từ chapters/ch5/main.tex (dòng 3033) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.6 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_06_lab_5_2_noi_suy import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 3: Commit bằng Merkle Tree
# ============================================================

def sha256_hash(*args):
    """Hash nối tiếp các giá trị."""
    h = hashlib.sha256()
    for a in args:
        h.update(str(a).encode())
    return h.hexdigest()[:16]  # Rút gọn cho dễ đọc

def build_merkle(leaves):
    """Xây Merkle tree, trả về (root, tree_layers)."""
    layers = [leaves[:]]
    current = leaves[:]
    # Pad to power of 2
    while len(current) & (len(current) - 1):
        current.append(current[-1])
    layers[0] = current[:]
    while len(current) > 1:
        next_layer = []
        for i in range(0, len(current), 2):
            next_layer.append(sha256_hash(current[i], current[i+1]))
        layers.append(next_layer)
        current = next_layer
    return current[0], layers

def get_proof(layers, index):
    """Merkle proof cho leaf index."""
    proof = []
    idx = index
    for layer in layers[:-1]:
        sibling = idx ^ 1
        if sibling < len(layer):
            proof.append((layer[sibling], idx % 2))
        idx //= 2
    return proof

# Hash các evaluation → Merkle tree
leaf_hashes = [sha256_hash(v) for v in extended_eval]
root, tree = build_merkle(leaf_hashes)

print(f"\n=== Merkle Commitment ===")
print(f"  Committed {len(extended_eval)} evaluations")
print(f"  Merkle root: {root}")
