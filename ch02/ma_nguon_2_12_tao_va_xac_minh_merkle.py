# Mã nguồn 2.12 - Tạo và xác minh Merkle proof
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 77
# Trích tự động từ chapters/ch2/main.tex (dòng 2425) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.11 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_11_ham_hash_va_xay_dung import *  # noqa
# --- Hết phần thêm ---

def get_merkle_proof(tree, index):
    """Trả về Merkle proof (danh sách sibling hash) cho lá index."""
    proof = []
    for level in tree[:-1]:
        sibling = index ^ 1  # XOR để lấy anh em
        if sibling >= len(level):
            sibling = index  # Nút lẻ cuối tầng: ghép với chính nó,
                             # khớp với build_merkle_tree
        proof.append((level[sibling], index % 2))
        index //= 2
    return proof

def verify_merkle_proof(leaf_hash, proof, root):
    """Xác minh Merkle proof."""
    h = leaf_hash
    for sibling_hash, is_left in proof:
        if is_left == 0:
            h = sha256(h, sibling_hash)
        else:
            h = sha256(sibling_hash, h)
    return h == root
