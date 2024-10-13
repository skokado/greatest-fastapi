from typing import Literal

from pydantic import BaseModel as BaseSchema


class LoginResponse(BaseSchema):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
