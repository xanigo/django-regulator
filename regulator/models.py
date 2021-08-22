from django.db.models import Model, TextField, IntegerField


class Rule(Model):
    calls = IntegerField(null=False)
    period = IntegerField(null=False)
    regex = TextField(null=False, unique=True)
