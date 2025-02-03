
# 智能医疗问答系统 💊

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green)](https://fastapi.tiangolo.com/)

一个基于真实医疗数据的智能问答系统，提供症状分类和药品建议服务。

## ✨ 主要功能

- **症状分类**：使用PubMedBERT模型进行症状分类
- **药品推荐**：根据症状匹配推荐药品
- **实时API**：提供即时的医疗建议查询
- **真实数据**：预设合理症状-药品映射关系
- **本地运行**：无需Docker，开箱即用

## 🚀 快速开始

### 环境要求

- Python 3.10+
- SQLite3
- (可选) NVIDIA GPU + CUDA 11.8

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/yourname/medical-ai-agent
cd medical-ai-agent

# 安装依赖
pip install -r requirements.txt

# (GPU用户) 安装PyTorch CUDA版
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 数据准备

```bash
# 生成模拟数据
python data/fake_data_generator.py

# 输出示例
✅ 已生成：
   - 症状数据：144 条
   - 药品数据：423 条
```

### 训练症状分类模型

```bash
python models/symptom_classifier/train.py

# 预期输出
🚀 开始训练...
Epoch | Train Loss | Val Accuracy
---------------------------------
1     | 0.8521     | 0.85
2     | 0.6325     | 0.90
...
💾 模型已保存到 models/symptom_classifier
```

### 启动API服务

```bash
uvicorn app.main:app --reload
```

访问以下地址进行测试：
- 📚 交互式API文档：http://localhost:8000/docs
- 🚦 服务状态检查：http://localhost:8000/healthcheck

## 📡 API使用示例

### 获取药品建议

```bash
curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"text":"我头痛应该吃什么药？"}'
```

**响应示例**：
```json
{
  "question": "我头痛应该吃什么药？",
  "advice": "建议考虑：布洛芬缓释胶囊 (300mg/次，每日2次)",
  "confidence": 0.97
}
```

### 症状分类

```bash
curl -X POST "http://localhost:8000/classify" \
-H "Content-Type: application/json" \
-d '{"text":"最近总是胃胀和恶心"}'
```

**响应示例**：
```json
{
  "symptom": "胃胀和恶心",
  "category": "消化系统",
  "probability": 0.92
}
```

## 📂 项目结构

```
medical-ai-agent/
├── app/
│   ├── __init__.py
│   ├── main.py           # API主入口
│   └── schemas.py        # 数据模型定义
├── data/
│   ├── fake_data_generator.py  # 数据生成脚本
│   └── medical.db        # SQLite数据库
├── models/
│   └── symptom_classifier/  # 训练好的模型
├── requirements.txt      # Python依赖
└── README.md             # 本说明文件
```

## 🚨 常见问题

### 中文显示乱码？

在启动命令中指定编码：
```bash
uvicorn app.main:app --reload --charset utf-8
```

### 如何添加新药品？

1. 编辑 `data/fake_data_generator.py` 中的 `MEDICAL_DATA` 字典
2. 重新生成数据：
```bash
python data/fake_data_generator.py
```

### GPU未使用？

检查PyTorch是否识别到CUDA：
```python
import torch
print(torch.cuda.is_available())  # 应输出True
```

如果显示False：
1. 确认已安装CUDA版PyTorch
2. 更新NVIDIA驱动
3. 重启服务

---

> ⚠️ 注意：本项目数据为模拟生成，不可作为真实医疗建议！如有健康问题请咨询专业医师。
