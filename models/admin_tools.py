from models.base import *

class CreateUserRequest(BaseModel):
    """Тело запроса на создание пользователя"""
    email: EmailStr = Field(..., description="Почта пользователя", examples=["bekhruz@zypl.ai"])


class CreatePartnerRequest(CreateUserRequest):
    name: str
    country: str = Field(..., description="ISO-3166 Alpha-2 код страны", min_length=2, max_length=2)
    engineer_ids: typing.Optional[typing.List[int]] = Field(..., description="ID профилей инженеров, работающих с текущим партнером")


class CreateEngineerRequest(CreateUserRequest):
    first_name: str
    last_name: str
    # middle_name: typing.Optional[str]
    