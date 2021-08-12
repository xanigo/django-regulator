from django.conf import settings

REDIS_DB: int = settings.REGULATOR['REDIS_DB']
DEFAULT_CALLS: int = settings.REGULATOR.get('DEFAULT_CALLS', 30)
DEFAULT_PERIOD: int = settings.REGULATOR.get('DEFAULT_PERIOD', 60)
