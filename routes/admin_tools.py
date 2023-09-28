from fastapi import APIRouter, Depends

from models.admin_tools import CreateEngineerRequest, CreatePartnerRequest
from models.users import UserOut
from db.users import User
from value_types import ProfileType
from services.facade import Services
from routes.middlewares import get_facade_services_if_authenticated


router = APIRouter(prefix="/admin", tags=['admin'])


@router.post("/engineers", response_model=UserOut)
async def create_engineer(body: CreateEngineerRequest,
                          services: Services = Depends(get_facade_services_if_authenticated)):
    """Запрос на создание аккаунта инженера"""
    engineer = await services.users.create_engineer(body.email, body.first_name, body.last_name)
    return await UserOut.from_tortoise_orm(engineer.user)


@router.post("/partners", response_model=UserOut)
async def create_partner(body: CreatePartnerRequest, 
                         services: Services = Depends(get_facade_services_if_authenticated)):
    """Запрос на создание аккаунта партнера"""
    partner = await services.users.create_partner(body.email, body.name, body.country, body.engineer_ids)
    return await UserOut.from_tortoise_orm(partner.user)