from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime

class TabInfoSchema(BaseModel):
    url: AnyHttpUrl
    time: datetime

    def __eq__(self, other):
        if isinstance(other, TabInfoSchema):
            return self.url == other.url
        return False