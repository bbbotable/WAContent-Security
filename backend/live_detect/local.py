# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
import os
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# 导入 Silent-Face-Anti-Spoofing 的活体检测类
import sys
sys.path.append(r"D:/4schoolwork/vscode/Content-Security/WAContent-Security/backend/live_detect/Silent-Face-Anti-Spoofing-master")
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage

# 创建 Blueprint
local_bp = Blueprint('local_bp', __name__)

# 配置模型路径和设备
MODEL_DIR = r"D:/4schoolwork/vscode/Content-Security/WAContent-Security/backend/live_detect/Silent-Face-Anti-Spoofing-master/resources/anti_spoof_models"
DEVICE_ID = -1  # 使用 CPU
THRESHOLD = 0.5  # 活体检测置信度阈值

@local_bp.route('/local', methods=['POST'])
def liveness_local():
    # 调试：确认收到请求
    print("收到 POST 请求到 /local")

    # 获取上传的图片
    image_file = request.files.get('image')
    if not image_file:
        print("错误：未收到上传的图片")
        return jsonify({"error": "No image uploaded"}), 400

    try:
        # 读取图片
        print("开始读取图片...")
        image_data = image_file.read()
        print(f"图片数据大小: {len(image_data)} 字节")
        image = Image.open(BytesIO(image_data))
        print("图片成功加载为 PIL Image")
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        print(f"图片转换为 OpenCV 格式，形状: {image.shape}")

        # 初始化活体检测器
        print("初始化 AntiSpoofPredict 检测器...")
        detector = AntiSpoofPredict(DEVICE_ID)
        print(f"检测器初始化完成，使用设备: {'CPU' if DEVICE_ID == -1 else f'CUDA:{DEVICE_ID}'}")

        # 人脸检测
        print("执行人脸检测...")
        image_bbox = detector.get_bbox(image)
        if image_bbox is None:
            print("错误：未检测到人脸")
            return jsonify({"error": "No face detected"}), 400
        print(f"人脸检测成功，边界框: {image_bbox}")

        # 裁剪人脸区域
        print("裁剪人脸区域...")
        cropper = CropImage()
        image_crop = cropper.crop(image, image_bbox, scale=2.7, out_w=80, out_h=80)
        print(f"人脸区域裁剪完成，形状: {image_crop.shape}")

        # 加载模型并预测
        print(f"扫描模型目录: {MODEL_DIR}")
        model_files = [f for f in os.listdir(MODEL_DIR) if f.endswith('.pth')]
        if not model_files:
            print(f"错误：模型目录 {MODEL_DIR} 中未找到 .pth 文件")
            return jsonify({"error": "No model files found in model_dir"}), 500
        print(f"找到模型文件: {model_files}")

        predictions = []
        for model_name in model_files:
            model_path = os.path.join(MODEL_DIR, model_name)
            print(f"加载模型: {model_path}")
            score = detector.predict(image_crop, model_path)
            print(f"模型 {model_name} 预测完成，分数: {score}")
            predictions.append(score[0][1])  # 提取活体置信度（索引 1 表示 live）

        # 融合多模型预测结果
        print(f"所有模型预测结果: {predictions}")
        final_score = np.mean(predictions)
        liveness_passed =  bool(final_score >= THRESHOLD)
        print(f"最终活体分数: {final_score}, 是否通过: {liveness_passed}")

        # 将 image_bbox 转换为 Python 原生类型
        image_bbox = [int(x) for x in image_bbox]  # 转换为整数列表
        print(f"转换后的边界框: {image_bbox}")

        # 返回结果
        response = {
            "liveness_passed": liveness_passed,
            "face_liveness": float(final_score),
            "raw_response": {
                "model_predictions": {model: float(pred) for model, pred in zip(model_files, predictions)},
                "bbox": image_bbox
            }
        }
        print(f"返回 JSON 响应: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"处理失败，错误信息: {str(e)}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500