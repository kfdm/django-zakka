import json
from urllib.parse import urlencode

from django import template
from django.shortcuts import reverse

# The JSONEncoder from DRF handles quite a few types, so we default to that
# if available and if not fallback to the Django one which still handles some
# extra types
try:
    from rest_framework.utils.encoders import JSONEncoder
except ImportError:
    from django.core.serializers.json import DjangoJSONEncoder as JSONEncoder


register = template.Library()


@register.simple_tag(takes_context=True)
def qs(context, *args, **kwargs):
    # If an item is passed as args, we
    # convert it to a kwargs so we can
    # simplify our code
    qs = context["request"].GET.copy()
    if args:
        kwargs[args[0]] = args[1]
    for key in kwargs:
        if kwargs[key] is None:
            qs.pop(key)
        else:
            qs[key] = kwargs[key]
    return urlencode(qs)


@register.filter(name="prettyjson")
def prettyjson(value):
    if isinstance(value, str):
        value = json.loads(value)
    return json.dumps(
        value,
        indent=2,
        sort_keys=True,
        cls=JSONEncoder,
    )


@register.simple_tag(takes_context=True)
def fullurl(context, viewname, *args, **kwargs):
    return context["request"].build_absolute_uri(
        reverse(viewname, args=args, kwargs=kwargs)
    )
