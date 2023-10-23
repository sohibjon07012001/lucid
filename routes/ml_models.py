from fastapi import APIRouter
from db.users import User, Partner
from fastapi import APIRouter, UploadFile, Form, Depends, Path
from routes.middlewares import has_engineer_profile, has_partner_profile, is_authenticated, get_facade_services_if_authenticated
from services.facade import Services
from models.partners import MlMoldels
from db.ml_models import Ml_Models
import exceptions
import typing
router = APIRouter(prefix="/ml_model", tags=['ml_model'])



@router.post(
    '/ml_model_result'
)
async def upload_model_result(
    excel_file: UploadFile,
    pkl_file: UploadFile,
    data_id:int,
    facade: Services = Depends(get_facade_services_if_authenticated)
    ):
    return await facade.ml_models.create_ml_models(data_id,excel_file, pkl_file)



@router.get('/{data_id}')
async def get_ml_models_info(data_id: int,
                              facade: Services = Depends(get_facade_services_if_authenticated)):
    return await facade.ml_models.get_ml_models(data_id=data_id)


@router.delete('/ml_model/{ml_model}',
               responses=exceptions.make_schemas(exceptions.FORBIDDEN))
async def delete_ml_model(ml_model: str ,
                          facade: Services = Depends(get_facade_services_if_authenticated)):
    return await facade.ml_models.delete_ml_models(ml_model)
