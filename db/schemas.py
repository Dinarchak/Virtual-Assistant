from pydantic import BaseModel
from datetime import datetime

class BarQuerySchema(BaseModel):
    name: str
    delta: int

class ScaleQuerySchema(BaseModel):
    name: str
    start: datetime
    end: datetime

class DailyTimeSchema(BaseModel):
    name: str
    delta: int
    day: int