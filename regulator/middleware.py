import re
from typing import Callable, Any, Tuple

from django.http import HttpRequest
from redis import Redis

from regulator.models import Rule
from regulator.settings import REDIS_DB, DEFAULT_CALLS, DEFAULT_PERIOD

counter = Redis(db=REDIS_DB, encoding='utf-8')


class RegulatorMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self.rules = {rule.regex: rule.rate for rule in Rule.objects.all()}

    def get_rate(self, request: HttpRequest) -> Tuple[int, int]:
        symbols = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400,
            'w': 604800,
        }

        for regex, rate in self.rules.items():
            if re.match(regex, f'{request.method} {request.path}'):
                calls, symbol = rate.split('/')
                period = symbols[symbol]
                calls = int(calls)
                return calls, period

        return DEFAULT_CALLS, DEFAULT_PERIOD

    def __call__(self, request: HttpRequest) -> Any:
        k = f'{request.META.get("REMOTE_ADDR")}:{request.path}:{request.method}'

        calls, period = self.get_rate(request)

        if counter.exists(k):
            if int(counter.get(k)) >= calls:
                raise Exception('Too Man requests')
            counter.incr(k)
        else:
            counter.set(k, 1, ex=period)

        return self.get_response(request)
