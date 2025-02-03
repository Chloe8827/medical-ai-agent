from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"

class ChatRequest(BaseModel):
    text: str

class DrugQuery(BaseModel):
    symptom_code: str
    max_results: Optional[int] = 5

class DrugResponse(BaseModel):
    name: str
    dosage: str
    symptom_code: str