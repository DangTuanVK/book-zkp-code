# Mã nguồn 5.7 - Lab 5.3: Xây dựng Merkle tree để commit các evaluation và mở một vị trí
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 5, trang 252
# Trích tự động từ chapters/ch5/main.tex (dòng 3195) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 5.6 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_5_06_lab_5_2_mien_va import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# BƯỚC 3: Commit bằng Merkle Tree
# ============================================================
def sha256_hash(*args):
    """Hash nối tiếp các giá trị (rút gọn 16 ký tự hex cho dễ đọc)."""
    h = hashlib.sha256()
    for a in args:
        h.update(str(a).encode() + b"|")
    return h.hexdigest()[:16]

def build_merkle(values):
    """Xây Merkle tree trên 2^k giá trị, trả về (root, các tầng)."""
    layers = [[sha256_hash(v) for v in values]]
    while len(layers[-1]) > 1:
        cur = layers[-1]
        layers.append([sha256_hash(cur[i], cur[i + 1])
                       for i in range(0, len(cur), 2)])
    return layers[-1][0], layers

def get_proof(layers, index):
    """Đường Merkle (các nút anh em) cho lá index."""
    proof = []
    for layer in layers[:-1]:
        proof.append(layer[index ^ 1])
        index //= 2
    return proof

def verify_proof(root, index, value, proof):
    h = sha256_hash(value)
    for sib in proof:
        h = sha256_hash(h, sib) if index % 2 == 0 else sha256_hash(sib, h)
        index //= 2
    return h == root

root_t, tree_t = build_merkle(tL)
print("\n=== Merkle Commitment ===")
print(f"  Cam kết {len(tL)} giá trị của t|L, root = {root_t}")
pf = get_proof(tree_t, 3)
print(f"  Mở vị trí 3: t(L[3]) = {tL[3]}, đường Merkle {len(pf)} hash, "
      f"hợp lệ: {verify_proof(root_t, 3, tL[3], pf)}")
print(f"  Mở sai giá trị {tL[3] + 1}: hợp lệ: {verify_proof(root_t, 3, tL[3] + 1, pf)}")
