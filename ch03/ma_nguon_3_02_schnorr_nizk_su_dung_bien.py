# Mã nguồn 3.2 - Schnorr NIZK sử dụng biến đổi Fiat-Shamir
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 3, trang 101
# Trích tự động từ chapters/ch3/main.tex (dòng 862) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 3.1 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_3_01_thiet_lap_duong_cong_va import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# NON-INTERACTIVE SCHNORR (FIAT-SHAMIR)
# ============================================================

def point_to_bytes(P):
    """Chuyển điểm EC thành bytes để hash."""
    if P.is_infinity:
        return b'\x00'
    return f"{P.x.val},{P.y.val}".encode()

def fiat_shamir_challenge(G, H, a, order):
    """Tính challenge bằng hash (Fiat-Shamir).
    e = H(G || H || a) mod order"""
    data = point_to_bytes(G) + b"|" + \
           point_to_bytes(H) + b"|" + \
           point_to_bytes(a)
    h = hashlib.sha256(data).digest()
    # Chuyển hash thành số nguyên mod order
    e = int.from_bytes(h, 'big') % order
    if e == 0: e = 1  # Tránh e = 0
    return e

def schnorr_nizk_prove(G, H, x, order):
    """Tạo Schnorr NIZK proof."""
    # Bước 1: Commitment
    r = random.randint(1, order - 1)
    a = r * G

    # Bước 2: Challenge (Fiat-Shamir – tự tính)
    e = fiat_shamir_challenge(G, H, a, order)

    # Bước 3: Response
    z = (r + e * x) % order

    # Proof = (a, z) – chỉ 2 phần tử!
    return (a, z)

def schnorr_nizk_verify(G, H, proof, order):
    """Xác minh Schnorr NIZK proof."""
    a, z = proof

    # Tính lại challenge (Verifier cũng dùng Fiat-Shamir)
    e = fiat_shamir_challenge(G, H, a, order)

    # Kiểm tra: [z]G == a + [e]H
    lhs = z * G
    rhs = a + (e * H)
    return lhs == rhs

# --- Demo ---
print(f"\n{'='*50}")
print(f"SCHNORR NIZK (FIAT-SHAMIR)")
print(f"{'='*50}")

proof = schnorr_nizk_prove(G, H_public, x_secret, order)
a_proof, z_proof = proof
print(f"Proof: (a={a_proof}, z={z_proof})")
print(f"Proof size: 2 phần tử")

valid = schnorr_nizk_verify(G, H_public, proof, order)
print(f"Verification: {'ACCEPT' if valid else 'REJECT'}")

# Tạo nhiều proof – mỗi cái khác nhau (randomness r khác)
print(f"\n--- Tạo 5 proof khác nhau cho cùng statement ---")
for i in range(5):
    pi = schnorr_nizk_prove(G, H_public, x_secret, order)
    ok = schnorr_nizk_verify(G, H_public, pi, order)
    print(f"  Proof {i+1}: a={pi[0]}, z={pi[1]} → {ok}")
