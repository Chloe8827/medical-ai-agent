# data/fake_data_generator.py
import sqlite3
import random
from pathlib import Path
from faker import Faker

fake = Faker('zh_CN')

# 扩展的医疗数据模板
MEDICAL_KNOWLEDGE = {
    # 神经系统新增症状和药品
    "神经系统": {
        "symptoms": [
            "偏头痛", "紧张性头痛", "丛集性头痛", "眩晕症",
            "失眠症", "睡眠障碍", "神经痛", "帕金森震颤",
            "偏瘫", "面神经麻痹", "癫痫发作", "阿尔茨海默症"
        ],
        "drugs": [
            {"name": "布洛芬缓释胶囊", "dosage": "300mg/次，每日2次", "type": "镇痛药"},
            {"name": "佐匹克隆片", "dosage": "7.5mg/次，睡前服用", "type": "安眠药"},
            {"name": "卡马西平片", "dosage": "200mg/次，每日3次", "type": "抗癫痫药"},
            {"name": "多巴丝肼片", "dosage": "250mg/次，每日3次", "type": "抗帕金森药"}
        ]
    },
    # 呼吸系统新增数据
    "呼吸系统": {
        "symptoms": [
            "急性支气管炎", "慢性咳嗽", "过敏性鼻炎", "鼻窦炎",
            "哮喘发作", "肺炎", "肺气肿", "胸膜炎",
            "呼吸困难", "咯血", "胸腔积液", "睡眠呼吸暂停"
        ],
        "drugs": [
            {"name": "沙丁胺醇吸入剂", "dosage": "100μg/喷，需要时使用", "type": "支气管扩张剂"},
            {"name": "孟鲁司特钠片", "dosage": "10mg/次，睡前服用", "type": "抗过敏药"},
            {"name": "阿奇霉素干混悬剂", "dosage": "500mg/日，连服3天", "type": "抗生素"},
            {"name": "布地奈德鼻喷雾剂", "dosage": "每个鼻孔1喷，每日2次", "type": "皮质类固醇"}
        ]
    },
    # 消化系统新增数据
    "消化系统": {
        "symptoms": [
            "胃食管反流", "消化性溃疡", "急性胃肠炎", "肠易激综合征",
            "肝硬化", "胰腺炎", "胆结石", "便血",
            "黑便", "吞咽困难", "黄疸", "腹水"
        ],
        "drugs": [
            {"name": "雷贝拉唑钠肠溶片", "dosage": "20mg/次，每日1次", "type": "质子泵抑制剂"},
            {"name": "蒙脱石散", "dosage": "3g/次，每日3次", "type": "止泻药"},
            {"name": "多潘立酮片", "dosage": "10mg/次，每日3次", "type": "促胃动力药"},
            {"name": "熊去氧胆酸胶囊", "dosage": "250mg/次，每日2次", "type": "利胆药"}
        ]
    },
    # 新增心血管系统分类
    "心血管系统": {
        "symptoms": [
            "稳定性心绞痛", "急性心肌梗死", "心律失常", "高血压危象",
            "心力衰竭", "心肌炎", "深静脉血栓", "动脉硬化",
            "心悸", "晕厥", "下肢水肿", "间歇性跛行"
        ],
        "drugs": [
            {"name": "硝酸甘油片", "dosage": "0.5mg/次，舌下含服", "type": "血管扩张剂"},
            {"name": "阿司匹林肠溶片", "dosage": "100mg/次，每日1次", "type": "抗血小板药"},
            {"name": "阿托伐他汀钙片", "dosage": "20mg/次，每晚服用", "type": "降脂药"},
            {"name": "美托洛尔缓释片", "dosage": "47.5mg/次，每日1次", "type": "β受体阻滞剂"}
        ]
    }
}


def generate_medical_data():
    """生成更真实的医疗数据"""
    conn = sqlite3.connect('data/medical.db')
    c = conn.cursor()

    # 清空旧数据
    c.execute("DROP TABLE IF EXISTS symptoms")
    c.execute("DROP TABLE IF EXISTS drugs")

    # 优化后的表结构
    c.execute('''CREATE TABLE symptoms (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        severity INTEGER CHECK(severity BETWEEN 1 AND 3)
    )''')

    c.execute('''CREATE TABLE drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dosage TEXT,
        symptom_code TEXT,
        drug_class TEXT,
        contraindications TEXT,
        FOREIGN KEY(symptom_code) REFERENCES symptoms(code)
    )''')

    symptom_id = 0
    for category, data in MEDICAL_KNOWLEDGE.items():
        # 为每个症状生成3个严重程度
        for severity in [1, 2, 3]:
            for symptom in data["symptoms"]:
                symptom_id += 1
                code = f"{category[:3].upper()}{symptom_id:04d}"

                # 插入症状数据（包含严重程度）
                c.execute("INSERT INTO symptoms VALUES (?,?,?,?)",
                          (code, f"{symptom}（{severity}级）", category, severity))

                # 为每个症状关联2-4种药物
                for drug in random.sample(data["drugs"], k=random.randint(2, 4)):
                    c.execute('''INSERT INTO drugs 
                              (name, dosage, symptom_code, drug_class, contraindications) 
                              VALUES (?,?,?,?,?)''',
                              (
                                  drug["name"],
                                  drug["dosage"],
                                  code,
                                  drug["type"],
                                  random.choice(["孕妇禁用", "肝功能不全慎用", "无禁忌", "过敏者禁用"])
                              ))

    conn.commit()
    print(f"✅ 已生成：")
    print(f"   - 症状数据：{symptom_id} 条")
    print(f"   - 药品数据：{conn.execute('SELECT COUNT(*) FROM drugs').fetchone()[0]} 条")
    conn.close()


if __name__ == "__main__":
    # 创建数据目录
    Path("data").mkdir(exist_ok=True)

    # 生成数据
    generate_medical_data()