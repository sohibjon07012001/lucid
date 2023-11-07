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
    old_password: str = Field()
    new_password: str = Field(min_length=6, max_length=24)

class ChangeProfileRequest(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr


class CreateAdminRequest(BaseModel):
    email: EmailStr
    password: str = Field()
    first_name: str = Field()
    last_name: str = Field()