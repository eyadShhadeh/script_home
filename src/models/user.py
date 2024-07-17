from pydantic import BaseModel
from uuid import uuid4, UUID


class User(BaseModel):
    user_id: UUID = uuid4()
    first_name: str
    last_name: str
    address: str
    age: int
