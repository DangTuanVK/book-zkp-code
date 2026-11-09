# Mã nguồn 1.1 - Completeness, soundness error và tấn công grinding
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 1, trang 15
# Trích tự động từ chapters/ch1/main.tex (dòng 748) bằng extract.py; không sửa tay file này.

import hashlib
import random

rng = random.Random(2026)

# --- Phần 1: Hang Ali Baba, k vòng, chạy N lần ---
def ali_baba(k, biet_mat_khau):
    """Trả về True nếu Victor chấp nhận sau k vòng."""
    for _ in range(k):
        loi_vao = rng.choice("AB")        # Peggy chọn lối vào
        yeu_cau = rng.choice("AB")        # Victor chọn lối ra
        if biet_mat_khau:
            loi_ra = yeu_cau              # mở cửa, đi ra đúng lối
        else:
            loi_ra = loi_vao              # không qua được cửa
        if loi_ra != yeu_cau:
            return False                  # một vòng sai là từ chối
    return True

N = 100_000
print("k  | trung thực | gian lận  | (1/2)^k")
for k in (1, 2, 5, 10):
    t = sum(ali_baba(k, True) for _ in range(N)) / N
    g = sum(ali_baba(k, False) for _ in range(N)) / N
    print(f"{k:<2} | {t:<10.3f} | {g:<9.5f} | {0.5**k:.5f}")

# --- Phần 2: Fiat--Shamir và tấn công grinding ---
# Thử thách k bit = k bit đầu của SHA-256(commitment).
# Kẻ gian đoán trước k bit, thử commitment cho đến khi băm khớp.
def thu_thach(commitment, k):
    h = int.from_bytes(hashlib.sha256(commitment).digest(), "big")
    return h >> (256 - k)

def grinding(k):
    doan = rng.getrandbits(k)             # chuỗi lối ra kẻ gian chuẩn bị
    so_lan = 0
    while True:
        so_lan += 1
        c = rng.getrandbits(64).to_bytes(8, "big")
        if thu_thach(c, k) == doan:
            return so_lan

print("\nk bit | số lần băm trung bình | 2^k")
for k in (8, 12, 16):
    tb = sum(grinding(k) for _ in range(200)) / 200
    print(f"{k:<5} | {tb:<21.0f} | {2**k}")
