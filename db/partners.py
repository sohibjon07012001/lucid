from db.base import *


class Template(DBModel):
    id = fields.IntField(pk=True)
    partner = fields.ForeignKeyField('db.Partner', related_name="templates")
    file_url = fields.CharField(max_length=255)
    file_name = fields.CharField(max_length=255)
    uploaded_by = fields.ForeignKeyField('db.Engineer', null=True, related_name="uploaded_templates")
    
    
    class PydanticMeta:
        exclude = ('uploaded_by', )