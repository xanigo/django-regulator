import re
from typing import Callable, Any, Tuple

from django.http import HttpRequest, HttpResponse
from redis import Redis

from regulator.models import Rule
from regulator.settings import REDIS_DB, DEFAULT_CALLS, DEFAULT_PERIOD

counter = Redis(db=REDIS_DB, encoding='utf-8')


class RegulatorMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self.rules = Rule.objects.all().values()

    def get_rate(self, request: HttpRequest) -> Tuple[int, int]:
        for rule in self.rules:
            if re.match(rule['regex'], f'{request.method} {request.path}'):
                return rule['calls'], rule['period']

        return DEFAULT_CALLS, DEFAULT_PERIOD

    def __call__(self, request: HttpRequest) -> Any:
        k = f'{request.META.get("REMOTE_ADDR")}:{request.path}:{request.method}'

        calls, period = self.get_rate(request)

        if counter.exists(k):
            if int(counter.get(k)) >= calls:
                return HttpResponse(status=429)
            counter.incr(k)
        else:
            counter.set(k, 1, ex=period)

        return self.get_response(request)
