# Mã nguồn 3.1b - (phần nối tiếp của Mã nguồn 3.1)
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 3, trang 98
# Trích tự động từ chapters/ch3/main.tex (dòng 801) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 3.1 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_3_01_thiet_lap_duong_cong_va import *  # noqa
# --- Hết phần thêm ---

# ============================================================
# INTERACTIVE SCHNORR PROOF
# ============================================================

def schnorr_interactive_prove_commit(G, order):
    """Bước 1: Prover tạo commitment."""
    r = random.randint(1, order - 1)  # Randomness bí mật
    a = r * G                          # Commitment
    return a, r  # r giữ bí mật cho bước 3

def schnorr_interactive_challenge(order):
    """Bước 2: Verifier chọn challenge ngẫu nhiên."""
    e = random.randint(1, order - 1)
    return e

def schnorr_interactive_respond(r, e, x, order):
    """Bước 3: Prover tính response."""
    z = (r + e * x) % order
    return z

def schnorr_interactive_verify(G, H, a, e, z):
    """Bước 4: Verifier kiểm tra."""
    lhs = z * G          # g^z
    rhs = a + (e * H)    # a * h^e  (cộng điểm EC)
    return lhs == rhs

# --- Chạy giao thức ---
print(f"\n{'='*50}")
print(f"SCHNORR INTERACTIVE PROOF")
print(f"{'='*50}")

# Bước 1: Prover commit
a, r = schnorr_interactive_prove_commit(G, order)
print(f"1. Prover gửi commitment:  a = {a}")

# Bước 2: Verifier challenge
e = schnorr_interactive_challenge(order)
print(f"2. Verifier gửi challenge: e = {e}")

# Bước 3: Prover respond
z = schnorr_interactive_respond(r, e, x_secret, order)
print(f"3. Prover gửi response:    z = {z}")

# Bước 4: Verify
valid = schnorr_interactive_verify(G, H_public, a, e, z)
print(f"4. Verification: {'ACCEPT' if valid else 'REJECT'}")

# --- Thử với witness sai ---
x_fake = (x_secret + 1) % order
z_fake = schnorr_interactive_respond(r, e, x_fake, order)
valid_fake = schnorr_interactive_verify(G, H_public, a, e, z_fake)
print(f"\nVới witness giả (x={x_fake}): "
      f"{'ACCEPT' if valid_fake else 'REJECT'}")
