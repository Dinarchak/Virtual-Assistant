from pydantic import BaseModel
from datetime import datetime

class TabInfoSchema(BaseModel):
    url: str
    time: datetime

    def __eq__(self, other):
        if isinstance(other, TabInfoSchema):
            return self.url == other.url
        return False