import typing
from db.users import User, Engineer, Partner, Root
from value_types import UserRole
import pandas as pd
import exceptions
from models.auth import CreateAdminRequest
import uuid
import bcrypt


async def authenticate(email: str, password: str) -> User:
    user = await User.get_or_none(email=email).prefetch_related('engineer_profile', "partner_profile")
    if user is None:
        raise exceptions.USER_NOT_FOUND
    
    if user.password is None:
        raise exceptions.USER_HAS_NO_PASSWORD
    
    if not user.check_password(password):
        raise exceptions.INVALID_PASSWORD
    
    return user

async def change_password(user: User, old_password: str, new_password: str):
    if not user.check_password(old_password):
        raise exceptions.OLD_PASSWORDS_DO_NOT_MATCH
    user.set_password(new_password)
    await user.save()
    return user


async def change_profile(user: User, email:str, first_name: str, last_name: str ):
    # user.set_email(email)
    # related_matrix = await user.filter(engineer=self.services.user.engineer_profile).prefetch_related('partner', 'engineer')
    if user.is_engineer():
        # res = await 
        await Engineer.filter(user_id=user.id).update(first_name=first_name, last_name=last_name)
        user.set_email(email=email)
        await user.save()
        return user
    elif user.is_partner():
        await Partner.filter(user_id=user.id).update(name=first_name)
        user.set_email(email=email)
        await user.save()
        return user
    elif user.is_admin():
        await Root.filter(user_id=user.id).update(first_name=first_name, last_name=last_name)
        user.set_email(email=email)
        await user.save()
        return user
    else:
        raise exceptions.FORBIDDEN
    


async def create_admin(user: User, r:CreateAdminRequest):
    if user.is_admin():
        admin_id = uuid.uuid4()
        password = bcrypt.hashpw(r.password.encode(), bcrypt.gensalt()).decode()
        s = await User.create(id=admin_id, email=r.email, password=password, role="admin")
        a = await Root.create(first_name=r.first_name, last_name=r.last_name, user_id=admin_id)
        return a 