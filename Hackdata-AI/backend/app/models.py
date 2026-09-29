
from pydantic import BaseModel
from typing import Optional, List


class ColumnSchema(BaseModel):
    name: str
    type: str
    min: Optional[int] = None
    max: Optional[int] = None


class DatasetSchema(BaseModel):
    rows: int
    columns: List[ColumnSchema]


class GenerateRequest(BaseModel):
    prompt: str