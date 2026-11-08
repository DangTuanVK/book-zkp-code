# Mã nguồn 2.2 - Minh họa bài toán logarit rời rạc với số nguyên tố 256-bit
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 42
# Trích tự động từ chapters/ch2/main.tex (dòng 206) bằng extract.py; không sửa tay file này.

# === Thử với số nguyên tố lớn (256-bit) ===
# Đây là kích thước thực tế trong mật mã
p_large = 2**255 - 19  # Số nguyên tố của Curve25519
g = 9  # Generator phổ biến của Curve25519

# Chọn "bí mật" x ngẫu nhiên
import random
x_secret = random.randint(1, p_large - 1)

# Tính "public key" y = g^x mod p – rất nhanh
y_public = pow(g, x_secret, p_large)
print(f"Secret x: {x_secret}")
print(f"Public y: {y_public}")
print(f"Từ y, tìm lại x: BÀI TOÁN LOGARIT RỜI RẠC – cực kỳ khó!")
