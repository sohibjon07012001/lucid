from db.users import Partner
from db.partners import Template, Data
from models.base import *
from db.ml_models import Ml_Models

TemplateOut = pydantic_model_creator(Template, name='TemplateOut', exclude=('partner', "uploaded_by"))
PartnerOut = pydantic_model_creator(Partner, name="PartnerOut", exclude=('engineerpartners', 'engineer_matrix'))
DataOut = pydantic_model_creator(Data, name="DataOut", exclude=('partner','engineerpartners', 'engineer_matrix', "uploaded_by"))
MlMoldels = pydantic_model_creator(Ml_Models, name="MlMoldels", exclude=("engineer_matrix", "engineer_matrix", "data", "templates"))