from pydantic import BaseModel


class UserLoginScheme(BaseModel):
    username: str
    password: str
