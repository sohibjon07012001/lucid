from fastapi import Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

import config
from services import users
from db.users import User, EngineerPartner
from value_types import UserRole
import exceptions
from services.facade import Services


bearer = HTTPBearer(description="Bearer JWT-токен")


async def is_authenticated(token: HTTPAuthorizationCredentials = Depends(bearer)) -> User:
    """Serves as a middleware function for related routes.
    Validates bearer jwt-token and returns matching context User object"""
    try:
        payload = jwt.decode(token.credentials, config.JWT.SECRET, algorithms=[config.JWT.ALGORITHM])
        user_id = payload.get('sub')
        if user_id is None:
            raise exceptions.NOT_AUTHENTICATED
        user = await users.get_user_by(id=user_id)
        if not user:
            raise exceptions.NOT_AUTHENTICATED
        return user
    except jwt.PyJWTError:
        raise exceptions.NOT_AUTHENTICATED


async def is_user_role_admin(user: User = Depends(is_authenticated)) -> User:
    if user.role != UserRole.ADMIN:
        raise exceptions.FORBIDDEN
    return user


async def has_engineer_profile(user: User = Depends(is_authenticated)) -> User:
    if user.engineer_profile is None:
        raise exceptions.FORBIDDEN
    return user


async def has_partner_profile(user: User = Depends(is_authenticated)) -> User:
    if user.partner_profile is None:
        raise exceptions.FORBIDDEN
    return user


async def get_facade_services_if_authenticated(user: User = Depends(is_authenticated)) -> Services:
    return Services(user)