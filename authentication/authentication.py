from django.contrib.auth.models import User
from django.db import IntegrityError
from api.models import Account
from django.http import JsonResponse, HttpResponse, HttpResponseServerError, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
from utils.custom_decorators import require_post_params

@require_post_params(params=['username', 'password'])
def cw_login(request):
    '''
    USAGE:

    '''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    remember = request.POST.get('remember', 'false')

    user = authenticate(username=username, password=password)
    if user is not None:
        if remember == 'false':
            request.session.set_expiry(0)

        login(request, user)

        if user.is_active:
            # TODO: Do not redirct, send success
            return HttpResponse()
        else:
            return HttpResponseBadRequest(reason='Inactive user')
    else:
        # Return an 'invalid login' error message.
        return HttpResponseBadRequest(reason='Invalid username or password')

def cw_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@require_post_params(params=['username', 'password', 'email'])
def cw_register(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')

    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest(reason='An account exists for this email address.')

    if User.objects.filter(username=username).exists():
        return HttpResponseBadRequest(reason='Sorry, this username is taken.')

    try:
        User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        account = Account(user=user)
        account.save()
    except Exception as e:
        print str(e)
        return HttpResponseServerError(reason=str(e))

    try:
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse()

    except Exception as e:
        print str(e)
        return HttpResponseServerError(reason=str(e))
