# Mã nguồn 12.4 - Train model MNIST và export sang ONNX cho zkML
# Sách: Chứng minh mà không tiết lộ (TS. Đặng Minh Tuấn), Chương 12, trang 427
# Trích tự động từ chapters/ch12/main.tex (dòng 841) bằng extract.py; không sửa tay file này.

# === zkml_demo.py – Train + Export + Prove ===
import torch
import torch.nn as nn
import json

# 1. Train model đơn giản (MNIST digit classifier)
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28*28, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleNet()
# ... train trên MNIST (bỏ qua cho ngắn gọn) ...

# 2. Export sang ONNX
dummy_input = torch.randn(1, 1, 28, 28)
torch.onnx.export(model, dummy_input, "mnist_model.onnx",
                  input_names=["image"],
                  output_names=["logits"])
print("Model exported to mnist_model.onnx")

# 3. Tạo input data
test_image = torch.randn(1, 1, 28, 28)  # Random image
with torch.no_grad():
    output = model(test_image)
    predicted = output.argmax(dim=1).item()
print(f"Prediction: digit {predicted}")

# Export input cho EZKL
input_data = {"input_data": [test_image.flatten().tolist()]}
with open("input.json", "w") as f:
    json.dump(input_data, f)
