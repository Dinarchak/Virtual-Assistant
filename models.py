from tortoise.models import Model
from tortoise import fields

class ProcessType(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)

class Process(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    type = fields.ForeignKeyField('models.ProcessType', on_delete=fields.base.OnDelete.CASCADE)

class LifePeriods(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    start = fields.DatetimeField(auto_now_add=True)
    end = fields.DatetimeField(null=True)