from db.base import * 

class Ml_Models(DBModel):
    ml_model_name = fields.CharField(max_length=255)
    sample_size = fields.IntField(null=True)
    train_size = fields.IntField(null=True)
    test_size = fields.IntField(null=True)
    total_good = fields.IntField(null=True)
    total_bad = fields.IntField(null=True)
    test_good = fields.IntField(null=True)
    test_bad = fields.IntField(null=True)
    threshold = fields.FloatField(null=True)
    tn = fields.IntField(null=True)
    fn = fields.IntField(null=True)
    tp = fields.IntField(null=True)
    fp = fields.IntField(null=True)
    auc = fields.CharField(max_length=50,null=True)
    accuracy = fields.CharField(max_length=50,null=True)
    approval_rate = fields.CharField(max_length=50,null=True)
    real_npl = fields.CharField(max_length=50,null=True)
    ml_model_npl = fields.CharField(max_length=50,null=True)
    data = fields.ForeignKeyField('db.Data', related_name="data_id_ml_model") 
    ml_model_id = fields.CharField(max_length=255,null=True)


class Pkl_Models(DBModel):
    ml_model_id = fields.CharField(max_length=255)
    # ml_model = fields.ForeignKeyField('db.Ml_Models', to_field='ml_model_id', related_name='second_models')
    pkl_file_url = fields.CharField(max_length=255)
    pkl_file_name = fields.CharField(max_length=255)

