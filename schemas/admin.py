from pydantic import BaseModel
from typing import Optional


class Admin(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
