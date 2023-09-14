from fastapi import APIRouter, Depends
import typing

from models.admin_tools import CreateUserRequest
from models.auth import AuthCheckEmailRequest, AuthCheckEmailResponse, SignInRequest, TokenResponse, SetPasswordRequest
from models.users import UserOut, PartnerOut, EngineerOut
from value_types import ProfileType
from services.facade import Services
from routes.middlewares import get_facade_services_if_authenticated
import exceptions
from services import users


router = APIRouter(prefix="/users")


@router.get("/engineers", response_model=typing.List[EngineerOut])
async def get_all_engineers():
    engineers = await users.get_engineers_by()
    return [await EngineerOut.from_tortoise_orm(e) for e in engineers]


@router.get("/partners", response_model=typing.List[PartnerOut])
async def get_all_partners(services: Services = Depends(get_facade_services_if_authenticated)):
    partners = await services.partners.get_partners()
    return [await PartnerOut.from_tortoise_orm(p) for p in partners]