# 人脸识别与活体检测系统

本项目采用 **Vue.js** 作为前端框架，**Flask** 作为后端服务，集成人脸识别与活体检测功能。活体检测结合了百度活体检测API和Silent-Face-Anti-Spoof开源模型，支持人脸签到与管理员系统管理。

---

## 项目功能

- **人脸识别与活体检测页面**：通过摄像头完成签到时的人脸检测与活体检测。  
- **管理员登录页面**：安全登录后台管理系统。  
- **系统管理页面**：  
  - 上传人脸数据（学号、姓名及照片）录入数据库  
  - 查看签到记录（包含检测结果）  
  - 签到统计（应到人数、实到人数及最早签到人）

---

## 目录结构

```

├── Face-recognition          # 前端项目（Vue）
│   ├── src
│   │   ├── components        # 前端组件
│   │   ├── views             # 前端页面
│   │   ├── router            # 路由定义
│   │   └── stores            # 前端页面与通信分离
│   ├── package.json
│   └── ...
├── backend                   # 后端项目（Flask）
│   ├── app.py                # Flask应用入口
│   ├── requirements.txt      # 后端依赖
│   ├── dataset               # 数据库存储
│   ├── face                  # 人脸识别模块
│   ├── live_detect           # 活体检测模块（含开源模型）
│   └── user_manage           # 用户管理模块
└── README.md

````

---

## 启动指南

### 1. 环境准备

- Python 3.7+
- Node.js 14+

---

### 2. 启动后端

```bash
cd backend
python -m venv venv                # 创建虚拟环境（推荐）
source venv/bin/activate           # 激活虚拟环境（Linux/macOS）
venv\Scripts\activate              # Windows

pip install -r requirements.txt   # 安装依赖

# 配置百度活体检测API参数，编辑 live_detect/baidu.py，填写 API Key 和 Secret Key

python app.py                     # 启动后端服务，默认监听 http://127.0.0.1:5000
````

---

### 3. 启动前端

```bash
cd ../Face-recognition
npm install                      # 安装依赖
npm run dev                      # 启动开发服务器，默认 http://localhost:5173
```

---

### 4. 使用说明

* 访问前端页面，登录管理员账号进入管理后台。
* 上传人员人脸数据（学号、姓名及照片）。
* 进入签到页面完成活体检测签到。
* 在管理页面查看签到记录与统计信息。

---

## 备注

* 数据库文件位于 `backend/dataset/face.db`。
* 活体检测模型存放于 `backend/live_detect/Silent-Face-Anti-Spoofing-master/resources`。
* 确保网络环境可访问百度活体检测API。
* 请保证下载



---



github链接：https://github.com/bbbotable/WAContent-Security
