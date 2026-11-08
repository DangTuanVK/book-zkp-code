# Mã nguồn 8.28 - Tạo Merkle tree và input cho circuit bỏ phiếu
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 8, trang 294
# Trích tự động từ chapters/ch8/main.tex (dòng 1181) bằng extract.py; không sửa tay file này.

# === generate_input.py – Tạo input cho circuit ===
# (Chạy offline để tạo Merkle tree + witness)

import hashlib, json

# Giả lập Poseidon hash bằng SHA-256 (demo only!)
# Production: dùng thư viện poseidon-hash thật
def mock_poseidon(*args):
    h = hashlib.sha256()
    for a in args:
        h.update(str(a).encode())
    return int(h.hexdigest(), 16) % (2**254)  # Truncate to field

# 4 cử tri đăng ký
voters = []
for i in range(4):
    secret = 1000 + i
    nullifier = 2000 + i
    commitment = mock_poseidon(secret, nullifier)
    voters.append({
        'secret': secret,
        'nullifier': nullifier,
        'commitment': commitment
    })
    print(f"Voter {i}: commit = {commitment}")

# Xây Merkle tree (depth 2 cho 4 lá)
leaves = [v['commitment'] for v in voters]
# Level 1
n01 = mock_poseidon(leaves[0], leaves[1])
n23 = mock_poseidon(leaves[2], leaves[3])
# Root
root = mock_poseidon(n01, n23)
print(f"Merkle root: {root}")

# Voter 1 (index=1) muốn bỏ phiếu
voter_idx = 1
v = voters[voter_idx]
null_hash = mock_poseidon(v['nullifier'])

# Merkle proof cho voter 1 (index=1 → binary: 01)
# Path: leaf → level1(sibling=leaves[0]) → root(sibling=n23)
input_data = {
    "merkleRoot": str(root),
    "nullifierHash": str(null_hash),
    "vote": "1",  # Bỏ phiếu "Có"
    "secret": str(v['secret']),
    "nullifier": str(v['nullifier']),
    "pathElements": [str(leaves[0]), str(n23)],
    "pathIndices": ["1", "0"]
    # index 1: ở bên phải level 0, bên trái level 1
}

with open('input_vote.json', 'w') as f:
    json.dump(input_data, f, indent=2)
print(f"Input saved to input_vote.json")
