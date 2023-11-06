from abc import *
import typing
import pandas as pd
from fastapi import UploadFile
import uuid
from db.users import User, Partner, Engineer, EngineerPartner
from db.ml_models import Ml_Models, Pkl_Models
import exceptions
from services.azure_storage import upload_file
from services.facade import AbsMlModelsResultService



class Ml_Models_Service_Engineer(AbsMlModelsResultService):
    async def create_ml_models(self, data_id: int, excel_file: UploadFile, pkl_file: UploadFile):
        df = pd.read_excel(excel_file.file.read())
        df.columns =df.columns.str.lower()
        df.columns = df.columns.str.replace(" ", "_")
        ml_model_id = uuid.uuid4()
        to_insert = [Ml_Models(
                                ml_model_name=i["model_name"], 
                               data_id=data_id,
                               sample_size =  i["sample_size"],
                               train_size =  i["train_size"],
                               test_size =  i["test_size"],
                               total_good =  i["total_good"],
                               total_bad =  i["total_bad"],
                               test_good =  i["test_good"],
                               test_bad =  i["test_bad"],
                               threshold =  i["threshold"],
                               tn =  i["tn"],
                               fn =  i["fn"],
                               tp =  i["tp"],
                               fp =  i["fp"],
                               auc =  i["auc"],
                               accuracy = i["accuracy"],
                               approval_rate =  i["approval_rate"],
                               real_npl =  i["real_npl"],
                               ml_model_npl =  i["model_npl"],
                               ml_model_id=ml_model_id
                            ) for i in df.to_dict('records')]
        
        file_url = await upload_file(file=pkl_file.file, file_name=pkl_file.filename, file_type=pkl_file.content_type)
        await Pkl_Models.create(ml_model_id=ml_model_id, pkl_file_url=file_url, pkl_file_name=pkl_file.filename)
        return await Ml_Models.bulk_create(to_insert)

    async def delete_ml_models(self, ml_model_id: str) -> bool:
        Ml_Models().filter(ml_model_id=ml_model_id).delete()
        return await Ml_Models.filter(ml_model_id=ml_model_id).delete()

    async def get_ml_models(self, data_id: int):
        ress = await Ml_Models.filter(data_id=data_id).all().values()
        if len(ress)==0:
            return []
        df = pd.DataFrame(ress)
        dictt = {}
        for i, j in enumerate(df['ml_model_id'].unique()):
            dictt[f"model{i}"] = df[df['ml_model_id']==j].to_dict("records")
        return dictt 

        







class Ml_Models_Service_Admin(AbsMlModelsResultService):
    def create_ml_models(self, partner_id: int, excel_file: UploadFile, pkl_file: UploadFile):
        raise exceptions.FORBIDDEN

    def delete_ml_models(self, template_id: int):
        raise exceptions.FORBIDDEN

    async def get_ml_models(self, data_id: int):
        ress = await Ml_Models.filter(data_id=data_id).all().values()
        if len(ress)==0:
            return []
        df = pd.DataFrame(ress)
        dictt = {}
        for i, j in enumerate(df['ml_model_id'].unique()):
            dictt[f"model{i}"] = df[df['ml_model_id']==j].to_dict("records")
        return dictt 


class Ml_Models_Service_Partner(AbsMlModelsResultService):
    def create_ml_models(self, partner_id: int, excel_file: UploadFile, pkl_file: UploadFile):
        raise exceptions.FORBIDDEN

    def delete_ml_models(self, template_id: int):
        raise exceptions.FORBIDDEN

    def get_ml_models(self, partner_id: int):
        raise exceptions.FORBIDDEN




