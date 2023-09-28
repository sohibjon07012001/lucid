import typing
from db.users import User, Engineer, Partner, EngineerPartner, UserRole
from value_types import UserRole

import exceptions
from services.facade import SubService, AbsUserService




async def get_user_by(**kwargs) -> User:
    user = await User.get_or_none(**kwargs).prefetch_related('engineer_profile', "partner_profile")
    if user is None:
        raise exceptions.USER_NOT_FOUND
    return user


async def get_partners_by(**kwargs):
    return await Partner.filter(**kwargs)


async def get_engineers_by(**kwargs):
    return await Engineer.filter(**kwargs)


async def set_password(email: str, password: str) -> User:
    user = await get_user_by(email=email)
    
    if user.password is not None:
        raise exceptions.USER_ALREADY_SET_PASSWORD
    
    user.set_password(password)
    await user.save()
    
    return user


class UserService_Admin(AbsUserService):
    async def create_user(self, email: str, role: str = UserRole.USER) -> User:
        return await User.create(
            email=email, role=role
        )
    
    async def create_engineer(self, email: str, first_name: str, last_name: str) -> Engineer:
        user = await _create_user(email=email)
        engineer = await Engineer.create(user=user, first_name=first_name, last_name=last_name)
        return engineer
    
    async def create_partner(self, email: str, name: str, country: str, engineer_ids: typing.List[int] = None) -> Partner:
        user = await _create_user(email=email)
        partner = await Partner.create(user=user, name=name, country=country)
        
        matrix = []
        for engineer_id in engineer_ids:
            matrix.append(EngineerPartner(engineer_id=engineer_id, partner_id=partner.id))
            
        if matrix:
            await EngineerPartner.bulk_create(matrix)
        
        return partner


class UserService_Partner(AbsUserService):
    async def create_user(self, email: str, role: str = UserRole.USER) -> User:
        raise exceptions.FORBIDDEN
    
    async def create_engineer(self, email: str, first_name: str, last_name: str, middle_name: str = None) -> Engineer:
        raise exceptions.FORBIDDEN
    
    async def create_partner(self, email: str, name: str, country: str, engineer_ids: typing.List[int] = None) -> Partner:
        raise exceptions.FORBIDDEN


class UserService_Engineer(AbsUserService):
    async def create_user(self, email: str, role: str = UserRole.USER) -> User:
        raise exceptions.FORBIDDEN
    
    async def create_engineer(self, email: str, first_name: str, last_name: str, middle_name: str = None) -> Engineer:
        raise exceptions.FORBIDDEN
    
    async def create_partner(self, email: str, name: str, country: str, engineer_ids: typing.List[int] = None) -> Partner:
        raise exceptions.FORBIDDEN


async def _create_user(email: str, role: str = UserRole.USER) -> User:
    return await User.create(
        email=email, role=role
    )

# async def get_user_by(**kwargs) -> User:
#     user = await User.get_or_none(**kwargs).prefetch_related('engineer_profile', "partner_profile")
    
#     if user is None:
#         raise exceptions.USER_NOT_FOUND
    
#     return user


async def create_engineer(email: str, first_name: str, last_name: str, middle_name: typing.Optional[str] = None,
                          role: UserRole = UserRole.USER) -> Engineer:
    user = await _create_user(email=email, role=role)
    engineer = await Engineer.create(user=user, first_name=first_name, last_name=last_name, middle_name=middle_name)
    return engineer


async def create_partner(email: str, name: str, country: str, engineer_ids: typing.Optional[typing.List[int]] = None) -> Partner:
    user = await _create_user(email=email)
    partner = await Partner.create(user=user, name=name, country=country)
    
    matrix = []
    for engineer_id in engineer_ids:
        matrix.append(EngineerPartner(engineer_id=engineer_id, partner_id=partner.id))
        
    if matrix:
        await EngineerPartner.bulk_create(matrix)
    
    return partner
    


