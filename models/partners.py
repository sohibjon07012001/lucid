from db.users import Partner
from db.partners import Template
from models.base import *


TemplateOut = pydantic_model_creator(Template, name='TemplateOut', exclude=('partner', "uploaded_by"))
PartnerOut = pydantic_model_creator(Partner, name="PartnerOut", exclude=('engineerpartners', 'engineer_matrix'))