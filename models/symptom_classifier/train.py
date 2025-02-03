# models/symptom_classifier/train.py
# models/symptom_classifier/train.py
import sqlite3
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import torch
from torch.utils.data import Dataset

# 动态获取绝对路径
DB_PATH = Path(__file__).parent.parent.parent / "data" / "medical.db"

class SymptomDataset(Dataset):
    """自定义症状数据集加载器"""

    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


def load_data_from_db():
    """从SQLite数据库加载训练数据"""
    print(f"🔍 数据库路径：{DB_PATH}")

    if not DB_PATH.exists():
        raise FileNotFoundError(f"数据库文件不存在，请先运行 data/fake_data_generator.py 生成数据")

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    # 获取症状和分类数据
    c.execute("SELECT name, category FROM symptoms")
    rows = c.fetchall()

    # 转换分类标签
    categories = list(set([row[1] for row in rows]))
    category_to_id = {cat: idx for idx, cat in enumerate(categories)}

    texts = [row[0] for row in rows]
    labels = [category_to_id[row[1]] for row in rows]

    return texts, labels, category_to_id


def train():
    # 加载数据
    texts, labels, category_map = load_data_from_db()
    print(f"✅ 加载 {len(texts)} 条训练数据")
    print("📋 分类映射:", category_map)

    # 划分训练集/测试集
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    # 初始化分词器
    tokenizer = AutoTokenizer.from_pretrained("microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract")

    # 分词处理
    train_encodings = tokenizer(
        train_texts,
        truncation=True,
        padding=True,
        max_length=128
    )
    test_encodings = tokenizer(
        test_texts,
        truncation=True,
        padding=True,
        max_length=128
    )

    # 创建数据集
    train_dataset = SymptomDataset(train_encodings, train_labels)
    test_dataset = SymptomDataset(test_encodings, test_labels)

    # 初始化模型
    model = AutoModelForSequenceClassification.from_pretrained(
        "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract",
        num_labels=len(category_map)
    )

    # 训练参数
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=5,
        weight_decay=0.01,
        logging_dir="./logs",
        fp16=torch.cuda.is_available()
    )

    # 训练器
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )

    # 开始训练
    print("🚀 开始训练...")
    trainer.train()

    # 保存模型
    model.save_pretrained("../../models/symptom_classifier")
    tokenizer.save_pretrained("../../models/symptom_classifier")
    print("💾 模型已保存到 models/symptom_classifier")


if __name__ == "__main__":
    train()