from uuid import uuid4
from abc import *
import typing
from fastapi import UploadFile
from typing import Optional
from db.partners import Template, Data
from db.users import EngineerPartner, User
from services.azure_storage import upload_file
import exceptions



from services.facade import AbsTemplateService


class TemplateService_Partner(AbsTemplateService):
    async def create_template(self, partner_id: int, template_id:int,  file: UploadFile) -> typing.List[Template]:
        file_url = await upload_file(file=file.file, file_name=file.filename, file_type=file.content_type)
        res =  await Data.create(
            partner_id=partner_id,
            template_id=template_id, 
            # uploaded_by_id=self.services.user.partner_profile.id,
            file_name=file.filename,
            file_url=file_url, 
        )
        return res,0
        # raise exceptions.FORBIDDEN
    
    async def get_templates(self, partner_id: int) -> typing.List[Template]:
        """Returns all the templates related to the given partner"""
        partner_id = self.services.user.partner_profile.id
        return await Template.filter(partner_id=partner_id)
    
    async def delete_template(self, template_id: int) -> bool:
        # try:
            # print("deleting_data")
            # return await Template.filter(id=template_id, partner_id=self.services.user.partner_profile.id).delete()
        return await Data().filter(id=template_id).delete()
        # except: 
        #     raise False



class TemplateService_Admin(AbsTemplateService):
    async def create_template(self, partner_id: int, file: UploadFile) -> Template:
        raise exceptions.FORBIDDEN
    
    async def get_templates(self, partner_id: int) -> typing.List[Template]:
        """Returns all the templates related to the given partner"""
        templates = await Template.filter(partner_id=partner_id)
        return templates
    
    async def delete_template(self, template_id: int) -> bool:
        return await Template.filter(id=template_id).delete()
        return True
    


class TemplateService_Engineer(AbsTemplateService):
    async def _is_engineer_related_to_partner(self, partner_id: int, engineer_id: int) -> bool:
        has_right_to = await EngineerPartner.get_or_none(partner_id=partner_id, engineer_id=engineer_id)
        if has_right_to is None:
            return False
        return True
    
    async def create_template(self, partner_id: int, file: UploadFile, template_id:int) -> Template:
        if not await self._is_engineer_related_to_partner(partner_id=partner_id, engineer_id=self.services.user.engineer_profile.id):
            raise exceptions.FORBIDDEN
        
        file_url = await upload_file(file=file.file, file_name=uuid4().__str__(), file_type=file.content_type)
        res = await Template.create(
            partner_id=partner_id, 
            uploaded_by_id=self.services.user.engineer_profile.id,
            file_name=file.filename,
            file_url=file_url, 
        )
        return res, 1
    
    async def get_templates(self, partner_id: int) -> typing.List[Template]:
        """Returns only templates that were uploaded by the given engineer"""
        templates = await Template.filter(partner_id=partner_id, uploaded_by_id=self.services.user.engineer_profile.id)
        return templates
    
    async def delete_template(self, template_id: int) -> bool:
        return await Template.filter(id=template_id, uploaded_by_id=self.services.user.engineer_profile.id).delete()
        return True