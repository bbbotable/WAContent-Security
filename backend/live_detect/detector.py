import cv2
import numpy as np
import torch
from pathlib import Path

class SilentFaceAntiSpoofing:
    def __init__(self, model_path=r"D:\4schoolwork\vscode\Content-Security\WAContent-Security\backend\live_detect\model\anti_spoof.pth"):
        # 验证模型文件是否存在
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        # 加载 PyTorch 模型
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model(model_path).to(self.device)
        self.model.eval()
        
        # 图像预处理参数
        self.input_size = (80, 80)  # MiniFASNetV2 的输入尺寸
        self.mean = [0.5, 0.5, 0.5]
        self.std = [0.5, 0.5, 0.5]

    def load_model(self, model_path):
        # 加载 MiniFASNetV2 模型
        from .MiniFASNet import MiniFASNetV2

        model = MiniFASNetV2(conv6_kernel=(5, 5))

        state_dict = torch.load(model_path, map_location=self.device)
        # 移除可能存在的 "module." 前缀
        new_state_dict = {k[7:] if k.startswith("module.") else k: v for k, v in state_dict.items()}
        model.load_state_dict(new_state_dict)
        return model

    def preprocess(self, image):
        # 调整大小
        image = cv2.resize(image, self.input_size)
        # 转换为浮点数
        image = image.astype(np.float32) / 255.0
        # 归一化
        image = (image - self.mean) / self.std
        # 转换为模型输入格式 (C, H, W)
        image = image.transpose(2, 0, 1)
        image = torch.from_numpy(image).float().unsqueeze(0).to(self.device)
        return image

    def predict(self, image):
        # 预处理图像
        input_data = self.preprocess(image)
        
        # 运行推理
        with torch.no_grad():
            # 获取原始输出
            output = self.model(input_data)  # [1, 3]
            output = output.squeeze(0)       # -> [3]
            print(output)
            # 对第2和第3个值做 softmax（fake vs real）
            fake_score = output[1]
            real_score = output[2]

            # 使用 softmax 获得概率（可选）
            probs = torch.softmax(torch.tensor([fake_score, real_score]), dim=0)
            score = probs[1].item()  # 概率值，越接近1越是真人
        print(score)
        return score