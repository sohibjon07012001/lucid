import typing
from fastapi import APIRouter, UploadFile, Form, Depends, Path

from routes.middlewares import has_engineer_profile, has_partner_profile, is_authenticated, get_facade_services_if_authenticated
from models.partners import TemplateOut, PartnerOut, DataOut
from services import templates
from services.azure_storage import upload_file
from db.users import User, Partner
from db.partners import Template, Data
from value_types import ProfileType
from services import users, auth, jwt
from services.facade import Services
import exceptions



router = APIRouter(prefix="/partners")


@router.post('/{partner_id}/templates', 
            #  response_model=TemplateOut,
            #  responses=exceptions.make_schemas(exceptions.FORBIDDEN)
             )
async def upload_partner_template(partner_id: int,#Path(..., description="ID профиля партнера") 
                                  file: UploadFile,#=Form(..., description="Файл шаблона (template)")
                                  services: Services = Depends(get_facade_services_if_authenticated)):
    template = await services.templates.create_template(partner_id=partner_id, file=file)
    if template[1] == 0:
    
    # print(type(Data))
    # print(type(template) == "<class 'db.partners.Data'>")
        return await DataOut.from_tortoise_orm(template[0])
    else:
        return await TemplateOut.from_tortoise_orm(template[0])


@router.delete('/templates/{template_id}',
               responses=exceptions.make_schemas(exceptions.FORBIDDEN))
async def delete_template(template_id: int = Path(..., description="ID шаблона"),
                          facade: Services = Depends(get_facade_services_if_authenticated)):
    return await facade.templates.delete_template(template_id)


@router.get('/{partner_id}', response_model=PartnerOut,
            responses=exceptions.make_schemas(exceptions.PARTNER_NOT_FOUND))
async def get_partner_profile(partner_id: int = Path(..., description="ID профиля партнера"),
                              user: User = Depends(is_authenticated)):
    partner = await Partner.get_or_none(id=partner_id)
    if not partner:
        raise exceptions.PARTNER_NOT_FOUND
    return await PartnerOut.from_tortoise_orm(partner)