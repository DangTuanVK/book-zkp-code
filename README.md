# Mã nguồn Python của sách "Chứng minh mà không tiết lộ"

Mã nguồn đi kèm sách **Chứng minh mà không tiết lộ -- Lý thuyết và thực hành
Zero-Knowledge Proof** (TS. Đặng Minh Tuấn). Thư mục này chứa toàn bộ 54 khối
mã Python in trong sách. Mỗi file được đánh số đúng như "Mã nguồn X.Y" trong
sách và đã được chạy thử. Kết quả chạy được lưu trong `ket_qua/`.

## Cấu trúc

```
chXX/ma_nguon_X_YY_<ten>.py   mã nguồn X.Y của Chương X, giống hệt trong sách
ket_qua/chXX/ma_nguon_X_YY.txt   kết quả khi chạy (stdout, stderr)
ket_qua/chXX/ma_nguon_X_YY_tep/  file do mã nguồn tạo ra (json, onnx...)
ket_qua/BAO_CAO.md            bảng tổng hợp: trang, nội dung, trạng thái
extract.py                    trích mã từ mã LaTeX của sách
resolve_deps.py               tìm phụ thuộc giữa các mã nguồn (deps.json)
run_all.py                    chạy tất cả, lưu kết quả, so với sách
```

Số mã nguồn trong sách đánh chung cho mọi ngôn ngữ (Python, Rust, Circom,
bash...), nên số của các file Python không liên tục: ví dụ Chương 4 có Mã
nguồn 4.1 đến 4.13, còn Chương 12 chỉ có Mã nguồn 12.4 là Python. Repo này
chỉ gồm mã Python; mã Circom, Rust (Halo2), Noir, Leo và Cairo trong sách
được chạy thử riêng với công cụ tương ứng. Một số khối
mã trong sách không có số riêng vì là phần nối tiếp của mã nguồn ngay trước;
các file này mang hậu tố `b`, ví dụ `ma_nguon_2_07b_...py`.

## Phụ thuộc giữa các mã nguồn

Một số mã nguồn dùng lại định nghĩa của mã nguồn trước, ví dụ lớp `Fp` (Mã
nguồn 2.14) được dùng trong lớp `ECPoint` (Mã nguồn 2.16), hay các phần của
một bài lab. Để mỗi file chạy độc lập được, đầu file có thêm một khối được
đánh dấu rõ:

```python
# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.14 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_14_lop_fp_hoan_chinh_truong import *  # noqa
# --- Hết phần thêm ---
```

Khối này nhập định nghĩa từ mã nguồn trước và tắt phần in ra của nó. Phần còn
lại của file giống hệt sách. Danh sách phụ thuộc nằm trong `deps.json`.

## Cài đặt và chạy

Phần lớn mã nguồn chỉ cần Python 3.10 trở lên với thư viện chuẩn. Ngoại lệ:
Mã nguồn 4.5 cần `numpy`; Mã nguồn 12.4 cần `torch` và `onnx`.

```bash
# Cách 1: conda / micromamba
micromamba env create -f environment.yml
micromamba run -n zkpbook python run_all.py

# Cách 2: pip
pip install numpy onnx
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
python run_all.py
```

Chạy một mã nguồn riêng lẻ (cần đứng trong thư mục chương để các dòng import
tìm thấy mã nguồn phụ thuộc):

```bash
cd ch02
python ma_nguon_2_08_noi_suy_lagrange_tren_truong.py
```

Chạy vài mã nguồn qua `run_all.py`: `python run_all.py 2_08 4_06`.

## Kết quả kiểm tra

Toàn bộ 54 mã nguồn chạy không lỗi với Python 3.10, numpy 2.2, torch 2.5.1.
Với 27 mã nguồn có in "Kết quả chạy" trong sách, kết quả thực tế trùng từng
dòng với sách. Chi tiết trong [ket_qua/BAO_CAO.md](ket_qua/BAO_CAO.md).

Một số mã nguồn dùng số ngẫu nhiên không cố định hạt giống hoặc đo thời gian
chạy, nên kết quả của bạn có thể khác các file trong `ket_qua/` ở những dòng
đó.

## Cập nhật khi sách thay đổi

Mã nguồn được trích tự động từ file LaTeX của sách, không chép tay. Khi sửa
mã trong sách:

```bash
python extract.py ../book-zkp       # trích lại từ thư mục sách
python resolve_deps.py              # chỉ cần khi có mã nguồn mới
python run_all.py
```

Mã nguồn trong sách nhằm minh họa: tham số nhỏ, không tối ưu, không an toàn để
dùng trong sản phẩm thực tế.

## Giấy phép

Mã nguồn được phát hành theo [giấy phép MIT](LICENSE). Nội dung sách (văn bản,
hình vẽ) không thuộc phạm vi giấy phép này.
