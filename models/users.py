from models.base import *
from db.users import User, Engineer, Partner


UserOut = pydantic_model_creator(User, name="UserOut", exclude=('password'))
EngineerOut = pydantic_model_creator(Engineer, name="EngineerOut", exclude=('user', ))
PartnerOut = pydantic_model_creator(Partner, name="PartnerOut", exclude=('user', ))
