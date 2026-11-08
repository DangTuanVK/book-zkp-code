# Mã nguồn 7.4 - Lab 7.4: Tổng hợp và so sánh kết quả benchmark
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 7, trang 287
# Trích tự động từ chapters/ch7/main.tex (dòng 617) bằng extract.py; không sửa tay file này.

# === lab7_results.py – Tổng hợp và trực quan hóa ===

# Điền kết quả đo được từ Lab 7.1--7.3
# (thay số dưới bằng kết quả thực từ máy bạn)
results = {
    'Groth16': {
        'prove_time_s': 1.2,     # Thay bằng số đo được
        'verify_time_ms': 3.5,
        'proof_size_bytes': 804,  # dạng JSON; nhị phân BN254: 256 B (không nén), 128 B (nén)
        'setup': 'circuit-specific',
    },
    'PLONK': {
        'prove_time_s': 2.1,
        'verify_time_ms': 5.2,
        'proof_size_bytes': 1580,
        'setup': 'universal',
    },
    'Noir (UltraPlonk)': {
        'prove_time_s': 1.8,
        'verify_time_ms': 4.8,
        'proof_size_bytes': 1200,
        'setup': 'universal',
    },
}

# === In bảng so sánh ===
print(f"{'Hệ thống':<20} {'Prove (s)':>10} {'Verify (ms)':>12} "
      f"{'Proof (B)':>10} {'Setup':>18}")
print("=" * 72)
for name, r in results.items():
    print(f"{name:<20} {r['prove_time_s']:>10.2f} "
          f"{r['verify_time_ms']:>12.1f} "
          f"{r['proof_size_bytes']:>10} "
          f"{r['setup']:>18}")

# === Phân tích ===
print(f"\n=== Phân tích ===")
fastest_prover = min(results, key=lambda k: results[k]['prove_time_s'])
smallest_proof = min(results, key=lambda k: results[k]['proof_size_bytes'])
fastest_verify = min(results, key=lambda k: results[k]['verify_time_ms'])

print(f"  Prover nhanh nhất:  {fastest_prover}")
print(f"  Proof nhỏ nhất:     {smallest_proof}")
print(f"  Verify nhanh nhất:  {fastest_verify}")

# === Scale test: thay đổi circuit size ===
print(f"\n=== Thử thay đổi kích thước circuit ===")
print(f"Sửa PoseidonChain(n) với n = 10, 50, 100, 500")
print(f"Chạy lại Lab 7.1--7.3 cho mỗi n")
print(f"Vẽ biểu đồ prove_time vs n để thấy scaling behavior")

sizes = [10, 50, 100, 500]
print(f"\n{'n':>5} {'~Constraints':>15} {'Groth16 (s)':>12} "
      f"{'PLONK (s)':>10}")
print("-" * 45)
for n in sizes:
    constraints = (n - 1) * 240  # PoseidonChain(n): n-1 lần hash, ~240 constraints/hash
    # Ước tính (thay bằng số đo thực)
    g16_time = n * 0.12
    plonk_time = n * 0.21
    print(f"{n:>5} {constraints:>15,} {g16_time:>12.1f} "
          f"{plonk_time:>10.1f}")
