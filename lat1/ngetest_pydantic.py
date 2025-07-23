from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str = "Sutaryo"
    signup_ts: Optional[datetime] = None
    friends: list[int] = []

external_data = {
    "id": "123",
    "signup_ts": "2025-07-07 10:00",
    "friends": [1,'2',b"3"]
}

user = User(**external_data)
print(user)
print(user.id)