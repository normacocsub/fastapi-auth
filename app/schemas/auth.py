from pydantic import BaseModel, EmailStr, constr


class Auth(BaseModel):
    email: EmailStr
    password: constr(min_length=3)
