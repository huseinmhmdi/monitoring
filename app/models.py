from tortoise.models import Model
from tortoise import fields

from enum import Enum


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class BaseModel(Model):
    id = fields.IntField(primary_key=True)

    class Meta:
        abstract = True


class DataSource(TimestampMixin, BaseModel):

    class Type(Enum):
        MYSQL = "mysql"
        REST = "rest"
        ELASTICSEARCH = "elasticsearch"

    name = fields.CharField(max_length=255)
    type = fields.CharEnumField(Type)
    args = fields.JSONField()


class Project(TimestampMixin, BaseModel):
    name = fields.CharField(max_length=255, unique=True)
    level_count = fields.IntField(default=0)


class Monitor(TimestampMixin, BaseModel):
    name = fields.CharField(max_length=255)
    source = fields.ForeignKeyField("models.DataSource", on_delete=fields.CASCADE, related_name="sources", null=True)
    project = fields.ForeignKeyField("models.Project", on_delete=fields.CASCADE, related_name="monitor--project")
    query = fields.CharField(max_length=1000)
    interval = fields.IntField(default=0)
    is_active = fields.BooleanField(default=True)


class Operator(TimestampMixin, BaseModel):
    class Type(Enum):
        SMS = "sms"
        EMAIL = "email"
        CALL = "call"
        REST = "rest"

    name = fields.CharField(max_length=255)
    type = fields.CharEnumField(Type)
    args = fields.JSONField()


class Alert(TimestampMixin, BaseModel):
    class Status(Enum):
        RESULVED = "resulved"
        FIRING = "firing"
        WARNING = "warning"

    monitor = fields.ForeignKeyField("models.Monitor", on_delete=fields.CASCADE, related_name="monitor")
    operator = fields.ForeignKeyField("models.Operator", on_delete=fields.CASCADE, related_name="operator")
    name = fields.CharField(max_length=255)
    condition = fields.CharField(max_length=255)
    duration = fields.IntField(default=0)
    tolerance = fields.IntField(default=0)
    status = fields.CharEnumField(Status)
    level = fields.IntField(default=0)


class AlertOperatorResult(TimestampMixin, BaseModel):
    alert = fields.ForeignKeyField("models.Alert", on_delete=fields.CASCADE, related_name="alert--operator")
    status = fields.BooleanField()
    description = fields.TextField(null=True)


class AlertResult(TimestampMixin, BaseModel):
    alert = fields.ForeignKeyField("models.Alert", on_delete=fields.CASCADE, related_name="alert--result")
    is_passed = fields.BooleanField(default=False)


class MontitorResult(TimestampMixin, BaseModel):
    monitor = fields.ForeignKeyField("models.Monitor", on_delete=fields.CASCADE, related_name="monitor--resoult")
    data = fields.JSONField()


class User(TimestampMixin, BaseModel):
    phone_number = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=255, null=True, unique=True)
    email = fields.CharField(max_length=255, null=True, unique=True)
    password = fields.CharField(max_length=255, null=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    father_name = fields.CharField(max_length=255, null=True)
    birth_daye = fields.DatetimeField(null=True)
    
