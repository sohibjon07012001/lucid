from fastapi import UploadFile
import typing
from abc import *

from db.users import User, Engineer, Partner, EngineerPartner, UserRole
from db.partners import Template
import exceptions

class UserBasedService(ABC):
    user: User
    
    def __init__(self, user: User, **kwargs):
        self.user = user
        super().__init__(**kwargs)


class SubService(ABC):
    services: 'Services'
    
    
    def __init__(self, services: 'Services') -> None:
        self.services = services


class AbsTemplateService(SubService, ABC):
    @abstractmethod
    async def create_template(self, partner_id: int, file: UploadFile) -> Template: ...
    
    @abstractmethod
    async def get_templates(self, partner_id: int) -> typing.List[Template]: ...
    
    @abstractmethod
    async def delete_template(self, template_id: int) -> bool: ...


class AbsUserService(SubService, ABC):    
    @abstractmethod
    async def create_user(email: str, role: str = UserRole.USER) -> User: ...
    
    @abstractmethod
    async def create_engineer(email: str, first_name: str, last_name: str, middle_name: typing.Optional[str] = None) -> Engineer: ...
    
    @abstractmethod
    async def create_partner(email: str, name: str, country: str, engineer_ids: typing.Optional[typing.List[int]] = None) -> Partner: ...
        


class AbsPartnerService(SubService, ABC):
    @abstractmethod
    async def get_partners(self) -> typing.List[Partner]: ...



class Services(UserBasedService):
    user: User
    templates: AbsTemplateService
    partners: AbsPartnerService
    users: AbsUserService
    
    def __init__(self, user: User, **kwargs):
        super().__init__(user, **kwargs)
        
        from services.templates import TemplateService_Admin, TemplateService_Engineer, TemplateService_Partner
        from services.partners import PartnerService_Admin, PartnerService_Engineer, PartnerService_Partner
        from services.users import  UserService_Admin, UserService_Engineer, UserService_Partner
        
        if self.user.is_admin():
            self.templates = TemplateService_Admin(self)
            self.partners = PartnerService_Admin(self)
            self.users = UserService_Admin(self)
        
        elif self.user.is_partner():
            self.templates = TemplateService_Partner(self)
            self.partners = PartnerService_Partner(self)
            self.users = UserService_Partner(self)
            print("is partner")
        elif self.user.is_engineer():
            self.templates = TemplateService_Engineer(self)
            self.partners = PartnerService_Engineer(self)
            self.users = UserService_Engineer(self)
            print("is engineer")
        else:
            print("FAILE")
          