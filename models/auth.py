from models.base import *
from models.users import UserOut

class AuthCheckEmailRequest(BaseModel):
    email: EmailStr


class AuthCheckEmailResponse(BaseModel):
    email: EmailStr
    has_password: bool


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str
    user: UserOut


class SetPasswordRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)


class ChangePasswordRequest(BaseModel):
    password: str = Field(min_length=6, max_length=24)
    password_cnf: str = Field(min_length=6, max_length=24)