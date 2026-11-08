# Mã nguồn 2.11 - Hàm hash và xây dựng cây Merkle
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 75
# Trích tự động từ chapters/ch2/main.tex (dòng 2259) bằng extract.py; không sửa tay file này.

import hashlib

def sha256(*args):
    """Hash nối tiếp các đầu vào."""
    h = hashlib.sha256()
    for a in args:
        h.update(a if isinstance(a, bytes) else a.encode())
    return h.digest()

def build_merkle_tree(leaves):
    """Xây cây Merkle, trả về list các tầng (tầng 0 = lá).
    Tầng có số nút lẻ: nút cuối được ghép với chính nó."""
    tree = [leaves]
    current = leaves
    while len(current) > 1:
        next_level = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i + 1] if i + 1 < len(current) else left
            next_level.append(sha256(left, right))
        tree.append(next_level)
        current = next_level
    return tree
