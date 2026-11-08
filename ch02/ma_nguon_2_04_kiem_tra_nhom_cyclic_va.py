# Mã nguồn 2.4 - Kiểm tra nhóm cyclic Z_7^* và phần tử sinh
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 2, trang 47
# Trích tự động từ chapters/ch2/main.tex (dòng 551) bằng extract.py; không sửa tay file này.

# === Kiểm tra nhóm cyclic Z_7^* ===
p = 7
g = 3  # Thử generator

print(f"Nhóm cyclic Z_{p}^* sinh bởi g = {g}:")
elements = set()
x = 1
for i in range(p - 1):
    elements.add(x)
    print(f"  {g}^{i} = {x}")
    x = (x * g) % p

# Kiểm tra: tạo đủ p-1 phần tử?
expected = set(range(1, p))
print(f"Sinh đủ tất cả phần tử? {elements == expected}")  # True
print(f"Bậc nhóm: {len(elements)}")                        # 6
