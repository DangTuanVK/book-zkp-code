# Mã nguồn 3.3 - Chứng minh DLEQ bằng giao thức Chaum-Pedersen NIZK
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 3, trang 109
# Trích tự động từ chapters/ch3/main.tex (dòng 1107) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 3.2 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_3_02_schnorr_nizk_su_dung_bien import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# CHAUM-PEDERSEN DLEQ NIZK
# Chứng minh: h1 = [x]G AND h2 = [x]F (cùng x)
# ============================================================

def dleq_nizk_prove(G, F, h1, h2, x, order):
    """DLEQ NIZK: chứng minh h1 = [x]G và h2 = [x]F."""
    r = random.randrange(order)
    a1 = r * G
    a2 = r * F

    # Fiat-Shamir: hash tất cả giá trị public
    data = b"|".join([point_to_bytes(v)
                      for v in [G, F, h1, h2, a1, a2]])
    h = hashlib.sha256(data).digest()
    e = int.from_bytes(h, 'big') % order
    if e == 0: e = 1

    z = (r + e * x) % order
    return (a1, a2, z)

def dleq_nizk_verify(G, F, h1, h2, proof, order):
    """Xác minh DLEQ NIZK proof."""
    a1, a2, z = proof

    data = b"|".join([point_to_bytes(v)
                      for v in [G, F, h1, h2, a1, a2]])
    h = hashlib.sha256(data).digest()
    e = int.from_bytes(h, 'big') % order
    if e == 0: e = 1

    # Kiểm tra CẢ HAI phương trình
    check1 = (z * G == a1 + (e * h1))
    check2 = (z * F == a2 + (e * h2))
    return check1 and check2

# --- Demo ---
print(f"\n{'='*50}")
print(f"CHAUM-PEDERSEN DLEQ NIZK")
print(f"{'='*50}")

x = random.randint(1, order - 1)
F = 5 * G  # Điểm cơ sở thứ hai (khác G)
h1 = x * G
h2 = x * F

print(f"Secret x = {x}")
print(f"h1 = [x]G = {h1}")
print(f"h2 = [x]F = {h2}")

proof = dleq_nizk_prove(G, F, h1, h2, x, order)
valid = dleq_nizk_verify(G, F, h1, h2, proof, order)
print(f"DLEQ Proof: valid = {valid}")

# Thử gian lận: h2 dùng x khác
h2_fake = (x + 3) * F  # x khác cho F
proof_fake = dleq_nizk_prove(G, F, h1, h2_fake, x, order)
valid_fake = dleq_nizk_verify(G, F, h1, h2_fake, proof_fake, order)
print(f"Gian lận (x khác nhau): valid = {valid_fake}")
