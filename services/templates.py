from uuid import uuid4
from abc import *
import typing
from fastapi import UploadFile
from typing import Optional
from db.partners import Template, Data
from db.users import EngineerPartner, User, Engineer, Partner
from services.azure_storage import upload_file
import exceptions
from services.email import SEND_EMAIL
from fastapi import FastAPI, BackgroundTasks
from tortoise.query_utils import Prefetch

from services.facade import AbsTemplateService


class TemplateService_Partner(AbsTemplateService):
    async def create_template(self, partner_id: int, template_id:int,  file: UploadFile) -> typing.List[Template]:
        w = await Template.filter(id=template_id).all().values_list("uploaded_by_id", flat=True)
        s = await Engineer.filter(id=w[0]).all().values_list("user_id", flat=True)
        a = await User.filter(id=s[0]).all().values_list("email", flat=True)
        send = SEND_EMAIL()
        send.send_emaill(message=f"{file.filename} uploaded, you can check template", send_to=a[0], subject="upload template")
        
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
        return await Data().filter(id=template_id).delete()


class TemplateService_Admin(AbsTemplateService):
    async def create_template(self, partner_id: int, file: UploadFile, template_id:int) -> Template:
        file_url = await upload_file(file=file.file, file_name=uuid4().__str__(), file_type=file.content_type)
        w = await Partner.filter(id=partner_id).values_list('user_id', flat=True)
        s =await User.filter(id=w[0]).values_list('email', flat=True)  
        send = SEND_EMAIL()
        send.send_emaill(message=f"{file.filename} uploaded, you can check template", send_to=s[0], subject="upload template")
        
        res = await Template.create(
            partner_id=partner_id, 
            # uploaded_by_id=self.services.user.engineer_profile.id,
            file_name=file.filename,
            file_url=file_url, 
        )
        return res, 1
        # raise exceptions.FORBIDDEN
    
    async def get_templates(self, partner_id: int) -> typing.List[Template]:
        """Returns all the templates related to the given partner"""
        templates = await Template.filter(partner_id=partner_id)
        return templates
    
    async def delete_template(self, template_id: int) -> bool:
        # return await Template.filter(id=template_id).delete()
        return await Data().filter(id=template_id).delete()
        # return True
    


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
        w = await Partner.filter(id=partner_id).values_list('user_id', flat=True)
        s =await User.filter(id=w[0]).values_list('email', flat=True)  
        send = SEND_EMAIL()
        send.send_emaill(message=f"{file.filename} uploaded, you can check template", send_to=s[0], subject="upload template")
        
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



