from db.base import *


class Template(DBModel):
    id = fields.IntField(pk=True)
    partner = fields.ForeignKeyField('db.Partner', related_name="templates")
    file_url = fields.CharField(max_length=255)
    file_name = fields.CharField(max_length=255)
    uploaded_by = fields.ForeignKeyField('db.Engineer', null=True, related_name="uploaded_templates")
    
    
    class PydanticMeta:
        exclude = ('uploaded_by')
    
class Data(DBModel):
    id = fields.IntField(pk=True)
    partner = fields.ForeignKeyField('db.Partner', related_name="data")
    template = fields.ForeignKeyField('db.Template', related_name="template_id_data") 
    file_url = fields.CharField(max_length=255)
    file_name = fields.CharField(max_length=255)
    is_valid = fields.BooleanField(null=True)
    initial_data_quantity = fields.IntField(null=True)
    number_of_string_data = fields.IntField(null=True)
    number_of_numeric_data = fields.IntField(null=True)
    error_commit = fields.CharField(max_length=500, null=True)


