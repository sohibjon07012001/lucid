import typing
from db.users import User, Engineer, Partner
from value_types import UserRole

import exceptions


async def authenticate(email: str, password: str) -> User:
    user = await User.get_or_none(email=email)
    if user is None:
        raise exceptions.USER_NOT_FOUND
    
    if user.password is None:
        raise exceptions.USER_HAS_NO_PASSWORD
    
    if not user.check_password(password):
        raise exceptions.INVALID_PASSWORD
    
    return user

async def change_password(user: User, password: str, password_cnf: str):
    if password != password_cnf:
        raise exceptions.PASSWORDS_DO_NOT_MATCH
    
    user.set_password(password)
    await user.save()