# Mã nguồn 2.2 - Minh họa bài toán logarit rời rạc với số nguyên tố 255-bit
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 43
# Trích tự động từ chapters/ch2/main.tex (dòng 208) bằng extract.py; không sửa tay file này.

# === Thử với số nguyên tố lớn (255-bit) ===
# Đây là kích thước thực tế trong mật mã
p_large = 2**255 - 19  # Một số nguyên tố 255-bit (trường cơ sở của Curve25519)
g = 2  # Cơ số nhỏ để minh họa, không cần là phần tử sinh của Z_p^*

# Chọn "bí mật" x ngẫu nhiên
import random
x_secret = random.randint(1, p_large - 1)

# Tính "public key" y = g^x mod p – rất nhanh
y_public = pow(g, x_secret, p_large)
print(f"Secret x: {x_secret}")
print(f"Public y: {y_public}")
print(f"Từ y, tìm lại x: BÀI TOÁN LOGARIT RỜI RẠC – cực kỳ khó!")
