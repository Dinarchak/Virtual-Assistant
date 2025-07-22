from pydantic import BaseModel
from datetime import datetime

class BarQuerySchema(BaseModel): # валидация?
    name: str
    delta: int


class ScaleQuerySchema(BaseModel): # валидация?
    name: str
    start: datetime
    end: datetime


class DailyTimeSchema(BaseModel): # валидация?
    name: str
    delta: int
    day: int

# class ProcessType(BaseModel):
