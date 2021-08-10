from django.conf import settings

REDIS_DB = settings.REGULATOR['REDIS_DB']
DEFAULT_CALLS = settings.REGULATOR.get('DEFAULT_CALLS', 30)
DEFAULT_PERIOD = settings.REGULATOR.get('DEFAULT_PERIOD', 60)
