import json
import datetime
import collections
from decimal import Decimal
from django.http import HttpResponse


def json_custom_parser(obj):
    """
    A custom json parser to handle json.dumps calls properly
    for Decimal and Datetime data types.
    """
    if isinstance(obj, Decimal):
        return str(obj)
    elif not isinstance(obj) and isinstance(obj, collections.Iterable):
        return list(obj)
    elif isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        dot_ix = 19  # 'YYYY-MM-DDTHH:MM:SS.mmmmmm+HH:MM'.find('.')
        return obj.isoformat()[:dot_ix]
    else:
        raise TypeError(obj)


def json_response(data, status=200):
    return HttpResponse(
        json.dumps(data, default=json_custom_parser),
        content_type="application/json",
        status=status,
    )
