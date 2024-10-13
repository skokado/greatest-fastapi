from datetime import datetime
from typing import Optional
from pydantic import BaseModel as BaseSchema


class UserRequest(BaseSchema):
    email: str
    password: str
    is_active: bool
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime


class UserResponse(BaseSchema):
    id: int
    email: str
    is_active: bool
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime
    updated_at: datetime
