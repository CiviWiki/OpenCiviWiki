from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url

'''
USAGE:
    @require_post_params(params=['we', 'are', 'required'])

    returns a bad request if all required parameters are not present in the POST
'''
def require_post_params(params):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if not all(param in request.POST for param in params):
                missing_params = " ".join([p for p in params if p not in request.POST])
                reason = "Missing required parameter(s): {p}".format(p=missing_params)
                return HttpResponseBadRequest(reason=reason)
            return func(request, *args, **kwargs)
        return inner
    return decorator

def beta_blocker(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_active:
            return HttpResponseRedirect('/beta')
        return func(request, *args, **kwargs)
    return inner
