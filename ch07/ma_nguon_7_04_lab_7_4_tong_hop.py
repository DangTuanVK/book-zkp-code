# Mã nguồn 7.4 - Lab 7.4: Tổng hợp và so sánh kết quả benchmark
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 7, trang 294
# Trích tự động từ chapters/ch7/main.tex (dòng 787) bằng extract.py; không sửa tay file này.

# === lab7_results.py – Tổng hợp và so sánh kết quả benchmark ===

# Kết quả đo trên máy của tác giả cho PoseidonChain(10) (Lab 7.1--7.3).
# Thay các số dưới bằng kết quả đo trên máy của bạn.
results = {
    'Groth16 (snarkjs)': {
        'prove_time_s': 1.9,      # thời gian lệnh snarkjs groth16 prove
        'verify_time_ms': 12,     # đo trong một tiến trình Node (không tính khởi động CLI)
        'proof_size_bytes': 804,  # JSON; nhị phân BN254: 256 B (không nén), 128 B (nén)
        'setup': 'circuit-specific',
    },
    'PLONK (snarkjs)': {
        'prove_time_s': 5.5,
        'verify_time_ms': 12,
        'proof_size_bytes': 2249,  # JSON; nhị phân: 9 G1 + 6 F_r ≈ 480 B (nén)
        'setup': 'universal',
    },
    'UltraHonk (Noir+bb)': {
        'prove_time_s': 0.28,      # bb prove với vk tạo sẵn
        'verify_time_ms': 10,
        'proof_size_bytes': 14656,  # tệp nhị phân target/proof
        'setup': 'universal',
    },
}

# === In bảng so sánh ===
print(f"{'Hệ thống':<20} {'Prove (s)':>10} {'Verify (ms)':>12} "
      f"{'Proof (B)':>10} {'Setup':>18}")
print("=" * 74)
for name, r in results.items():
    print(f"{name:<20} {r['prove_time_s']:>10.2f} "
          f"{r['verify_time_ms']:>12.1f} "
          f"{r['proof_size_bytes']:>10} "
          f"{r['setup']:>18}")

# === Phân tích ===
print("\n=== Phân tích ===")
fastest_prover = min(results, key=lambda k: results[k]['prove_time_s'])
smallest_proof = min(results, key=lambda k: results[k]['proof_size_bytes'])
fastest_verify = min(results, key=lambda k: results[k]['verify_time_ms'])

print(f"  Prover nhanh nhất:  {fastest_prover}")
print(f"  Proof nhỏ nhất:     {smallest_proof}")
print(f"  Verify nhanh nhất:  {fastest_verify}")

# === Scale test: kích thước circuit và ptau cần dùng ===
# Hệ số lấy từ số đo thực: mỗi Poseidon(2) của circomlib có
# 243 constraints phi tuyến + 274 constraints tuyến tính = 517 R1CS
# constraints; snarkjs chuyển thành 596 PLONK constraints; bb báo
# 927 gate UltraHonk cho mỗi lần hash_2 của noir-lang/poseidon.
def r1cs_constraints(n):
    return 517 * (n - 1)

def plonk_constraints(n):
    return 596 * (n - 1) + 1

def ultrahonk_gates(n):
    return 927 * (n - 1) + 19

# snarkjs yêu cầu 2^p >= (constraints + public input/output) với Groth16,
# 2^p >= số PLONK constraints với PLONK (p = số mũ của file ptau)
def ptau_power_groth16(n, n_public=1):
    return (r1cs_constraints(n) + n_public).bit_length()

def ptau_power_plonk(n):
    return (plonk_constraints(n) - 1).bit_length()

print("\n=== Kích thước circuit theo n (PoseidonChain(n)) ===")
print(f"{'n':>4} {'R1CS':>9} {'PLONK':>9} {'UltraHonk':>10} "
      f"{'ptau G16':>9} {'ptau PLONK':>11}")
print("-" * 57)
for n in [10, 50, 100, 500]:
    print(f"{n:>4} {r1cs_constraints(n):>9,} {plonk_constraints(n):>9,} "
          f"{ultrahonk_gates(n):>10,} {'2^' + str(ptau_power_groth16(n)):>9} "
          f"{'2^' + str(ptau_power_plonk(n)):>11}")
