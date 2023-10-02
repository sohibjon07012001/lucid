from enum import Enum

from db.base import *
# from db.partners import Template
from value_types import UserRole

import bcrypt


class User(DBModel):
    """Аккаунт пользователя"""
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=128, unique=True)
    password = fields.CharField(max_length=255, null=True)  # Password can be null before it has been set
    
    role = fields.CharEnumField(UserRole, max_length=128, default=UserRole.USER)
    
    engineer_profile: fields.OneToOneNullableRelation['Engineer']
    partner_profile: fields.OneToOneNullableRelation['Partner']
    def is_activated(self) -> bool:
        return self.password is not None
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
            
    def is_partner(self) -> bool:
        return self.partner_profile is not None
    
    def is_engineer(self) -> bool:
        print(self.engineer_profile.all().values())
        return self.engineer_profile is not None
    
    def check_password(self, password: str) -> bool:
        if self.password is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class Engineer(DBModel):
    """Профиль инженера"""
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('db.User', related_name='engineer_profile')
    
    first_name = fields.CharField(max_length=24)
    last_name = fields.CharField(max_length=24)
    # middle_name = fields.CharField(max_length=24, null=True)
    
    
    class PydanticMeta:
        exclude = ('uploaded_templates', )


class Partner(DBModel):
    """Профиль партнера"""
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('db.User', related_name="partner_profile")
    name = fields.CharField(max_length=64, unique=True)
    country = fields.CharField(max_length=3)
    
    # templates: fields.ForeignKeyRelation[Template]
    # engineer_matrix: fields.ForeignKeyRelation['EngineerPartner']
    

class EngineerPartner(DBModel):
    engineer = fields.ForeignKeyField('db.Engineer', related_name="partner_matrix")
    partner = fields.ForeignKeyField('db.Partner', related_name="engineer_matrix")
    
    class PydanticMeta:
        exclude = ('partner', 'engineer')
    
    class Meta:
        unique_together = ('engineer', 'partner')