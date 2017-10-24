#
#
# To generate a model for a new table use:
#     python -m pwiz -H 192.168.3.54 -u richard -P -e mysql -t <TABLE NAME> dvc

from peewee import *

dvc_db = MySQLDatabase(None)

def get_dvc_db():
    return dvc_db

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = dvc_db

class ActiveClient(BaseModel):
    client = IntegerField(db_column='Client_ID', null=True)
    date = DateField(null=True)

    class Meta:
        db_table = 'active_client'
        indexes = (
            (('date', 'client'), False),
            (('date', 'client'), True),
        )

class UpdateRunModel(BaseModel):
    datetime = DateTimeField(null=True)
    type = CharField(null=True)

    class Meta:
        db_table = 'update_run'
        indexes = (
            (('type', 'datetime'), False),
        )

class SmsText(BaseModel):
    client = IntegerField(db_column='client_id', null=True)
    content = TextField()
    created = DateTimeField(index=True)
    error_code = IntegerField()
    phone_mobile = CharField()
    retries = IntegerField()
    send_at = DateTimeField()
    status = CharField(index=True)
    text = PrimaryKeyField(db_column='text_id')
    updated = DateTimeField()

    class Meta:
        db_table = 'sms_texts'

