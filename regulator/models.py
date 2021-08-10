from django.db.models import TextField

from fancy.models import SafeDeleteModel, LogFieldsModel


class Rule(SafeDeleteModel, LogFieldsModel):
    rate = TextField()
    regex = TextField(null=False, unique=True)
