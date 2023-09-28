# from fastapi import APIRouter, UploadFile, Form, Depends, Path
# from models.partners import TemplateOut, PartnerOut, DataOut
# from services.facade import Services
# import typing
# from routes.middlewares import has_engineer_profile, has_partner_profile, is_authenticated, get_facade_services_if_authenticated

# router = APIRouter(prefix="/partners", tags=["partners"])

# @router.post('/{partner_id}/templates',
             
              
#             #  response_model=TemplateOut,
#             #  responses=exceptions.make_schemas(exceptions.FORBIDDEN)
#              )
# async def upload_partner_template(partner_id: int,#Path(..., description="ID профиля партнера") 
                                  
#                                   file: UploadFile,#=Form(..., description="Файл шаблона (template)")
#                                   template_id: typing.Optional[int]= None,
#                                   services: Services = Depends(get_facade_services_if_authenticated,),
#                                   ):
#     template = await services.templates.create_template(partner_id=partner_id, file=file, template_id=template_id)
#     if template[1] == 0:
#         return await DataOut.from_tortoise_orm(template[0])
#     else:
#         return await TemplateOut.from_tortoise_orm(template[0])
