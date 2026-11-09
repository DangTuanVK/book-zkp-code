# Mã nguồn 4.2 - Biểu diễn và tính toán arithmetic circuit cho x^3 + x + 5 = 35
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 4, trang 129
# Trích tự động từ chapters/ch4/main.tex (dòng 714) bằng extract.py; không sửa tay file này.

# === Arithmetic Circuit đơn giản ===

class Gate:
    """Một cổng trong arithmetic circuit."""
    def __init__(self, op, left, right, output):
        self.op = op          # 'mul' hoặc 'add'
        self.left = left      # Tên wire trái
        self.right = right    # Tên wire phải
        self.output = output  # Tên wire đầu ra

class ArithmeticCircuit:
    """Arithmetic circuit trên F_p."""
    def __init__(self, p):
        self.p = p
        self.gates = []

    def add_gate(self, op, left, right, output):
        self.gates.append(Gate(op, left, right, output))

    def evaluate(self, assignment):
        """Tính toán circuit, điền giá trị cho tất cả wire."""
        for gate in self.gates:
            l = assignment[gate.left]
            r = assignment[gate.right]
            if gate.op == 'mul':
                assignment[gate.output] = (l * r) % self.p
            elif gate.op == 'add':
                assignment[gate.output] = (l + r) % self.p
        return assignment

    def verify(self, assignment):
        """Kiểm tra assignment có thỏa mãn tất cả cổng."""
        for gate in self.gates:
            l = assignment[gate.left]
            r = assignment[gate.right]
            o = assignment[gate.output]
            if gate.op == 'mul':
                if (l * r) % self.p != o: return False
            elif gate.op == 'add':
                if (l + r) % self.p != o: return False
        return True

# === Ví dụ: x^3 + x + 5 = 35 ===
p = 41  # Số nguyên tố
circuit = ArithmeticCircuit(p)
circuit.add_gate('mul', 'x', 'x', 'w1')       # w1 = x * x
circuit.add_gate('mul', 'w1', 'x', 'w2')      # w2 = w1 * x = x^3
circuit.add_gate('add', 'w2', 'x', 'w3')      # w3 = w2 + x = x^3+x
circuit.add_gate('add', 'w3', 'five', 'w4')   # w4 = w3 + 5

# Witness: x = 3
assignment = {'x': 3, 'five': 5}
circuit.evaluate(assignment)
print(f"Assignment: {assignment}")
print(f"Circuit valid: {circuit.verify(assignment)}")
print(f"Output w4 = {assignment['w4']} (expected 35)")

# Witness sai: x = 4
bad = {'x': 4, 'five': 5}
circuit.evaluate(bad)
print(f"\nBad assignment (x=4): w4 = {bad['w4']} (≠ 35)")
