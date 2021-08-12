from django.db.models import Model, TextField


class Rule(Model):
    rate = TextField()
    regex = TextField(null=False, unique=True)
