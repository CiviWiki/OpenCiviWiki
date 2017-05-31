from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from api.models import Account
from django.http import JsonResponse, HttpResponse, HttpResponseServerError, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
from utils.custom_decorators import require_post_params
from reserved_usernames import RESERVED_USERNAMES
from forms import AccountRegistrationForm
from api.tasks import send_email
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.http import base36_to_int, int_to_base36

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import salted_hmac

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """ Token Generator for Email Confirmation """
    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
    def _make_token_with_timestamp(self, user, timestamp):
        """ Token function pulled from Django 1.11 """
        ts_b36 = int_to_base36(timestamp)

        hash = salted_hmac(
            self.key_salt,
            unicode(user.pk) + unicode(timestamp)
        ).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)

account_activation_token = AccountActivationTokenGenerator()


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
            # TODO: Do not redirect, send success
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
    form = AccountRegistrationForm(request.POST or None)
    if request.method == 'POST':
        # Form Validation
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password()
            email = form.clean_email()

            # Create a New Account
            try:
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                account = Account(user=user)
                account.save()

                user.is_active = True
                user.save()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                domain = get_current_site(request).domain
                base_url = "http://{domain}/auth/activate_account/{uid}/{token}/"
                url_with_code = base_url.format(domain=domain, uid=uid, token=token)
                # Send Email Verification Message
                # TODO: Move this to string templates
                email_context = {
                    'title' : 'Verify your email with CiviWiki',
                    'body' : "Welcome to CiviWiki! Follow the link below to verify your email with us. We're happy to have you on board :)",
                    'link': url_with_code
                }

                send_email.delay(
                    subject="CiviWiki Account Setup",
                    recipient_email=email,
                    context=email_context
                )

                login(request, user)
                return HttpResponse()

            except Exception as e:
                return HttpResponseServerError(reason=str(e))

        else:
            response = {
                'success': False,
                'errors' : [error[0] for error in form.errors.values()]
            }
            return JsonResponse(response, status=400)
    else:
        return HttpResponseBadRequest(reason="POST Method Required")

def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        account = Account.objects.get(user=user)
        account.is_verified = True
        account.save()

        return HttpResponse('Thanks! Your email address has been verified')
    else:
        # invalid link
        return HttpResponseBadRequest("INVALID VALUES")
