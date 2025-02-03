from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()


class ChatRequest(BaseModel):
    text: str


@app.post("/chat")
def simple_chat(request: ChatRequest):
    """极简版问答接口"""
    conn = sqlite3.connect('data/medical.db')
    c = conn.cursor()

    # 示例查询逻辑
    c.execute('SELECT name, dosage FROM drugs LIMIT 3')
    results = [f"{name} ({dosage})" for name, dosage in c.fetchall()]

    return {
        "question": request.text,
        "advice": "建议考虑：" + "、".join(results)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)