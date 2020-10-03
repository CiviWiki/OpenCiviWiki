from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse, HttpResponseServerError, HttpResponseRedirect, \
    HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse  # TODO: move this out to views
from django.utils.crypto import salted_hmac
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.http import int_to_base36
from django.views.decorators.debug import sensitive_post_parameters

from api.tasks import send_email
from api.models import Account, Invitation
from .forms import AccountRegistrationForm, PasswordResetForm, RecoverUserForm
from core.custom_decorators import require_post_params


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


@sensitive_post_parameters('password')
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

            account = get_object_or_404(Account, user=user)
            request.session["login_user_firstname"] = account.first_name
            request.session["login_user_image"] = account.profile_image_thumb_url

            return HttpResponse()
        else:
            response = {
                "message": 'Inactive user',
                "error": "USER_INACTIVE"
            }
            return JsonResponse(response, status=400)
    else:
        # Return an 'invalid login' error message.
        response = {
            "message": 'Invalid username or password',
            "error": "INVALID_LOGIN"
        }
        return JsonResponse(response, status=400)


def cw_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@sensitive_post_parameters('password')
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
                if not settings.CLOSED_BETA:
                    account.beta_access = True
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
                    'title': 'Verify your email with CiviWiki',
                    'body': ("Welcome to CiviWiki! Follow the link below to verify your email with us. "
                             "We're happy to have you on board :)"),
                    'link': url_with_code
                }

                send_email.delay(
                    subject="CiviWiki Account Setup",
                    recipient_list=[email],
                    context=email_context
                )

                login(request, user)
                return HttpResponse()

            except Exception as e:
                return HttpResponseServerError(reason=str(e))

        else:
            response = {
                'success': False,
                'errors': [error[0] for error in form.errors.values()]
            }
            return JsonResponse(response, status=400)
    else:
        return HttpResponseBadRequest(reason="POST Method Required")


@sensitive_post_parameters('password')
@require_post_params(params=['username', 'password', 'email', 'beta_token'])
def beta_register(request):
    """ Special registration request for beta access """
    # Beta Check
    beta_token = request.POST.get('beta_token', '')
    if beta_token:
        email = request.POST.get('email' '')
        try:
            invitation = Invitation.objects.get(invitee_email=email)
        except Invitation.DoesNotExist:
            response_data = {
                "message": "Beta invitation does not exist for this email",
                "error": "NO_BETA_INVITE"
            }
            return JsonResponse(response_data, status=400)

        if invitation.verification_code != beta_token:
            response_data = {
                "message": "The beta token is not valid",
                "error": "INVALID_BETA_TOKEN"
            }
            return JsonResponse(response_data, status=400)

    else:
        response_data = {
            "message": "Missing Beta Token",
            "error": "MISSING_BETA_TOKEN"
        }
        return JsonResponse(response_data, status=400)

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
                account.beta_access = True
                account.is_verfied = True
                account.save()

                invitation = Invitation.objects.get(invitee_email=email)
                invitation.invitee_user = user
                invitation.save()

                user.is_active = True
                user.save()

                login(request, user)
                return HttpResponse()

            except Exception as e:
                return HttpResponseServerError(reason=str(e))

        else:
            response = {
                'success': False,
                'errors': [error[0] for error in form.errors.values()]
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
        if account.is_verified:
            redirect_link = {
                'href': "/",
                'label': "Back to Main"
            }
            template_var = {
                'title': "Email Already Verified",
                'content': "You have already verified your email",
                'link': redirect_link
            }
            return TemplateResponse(request, 'general-message.html', template_var)
        else:
            account.is_verified = True
            account.save()

            redirect_link = {
                'href': "/",
                'label': "Back to Main"
            }
            template_var = {
                'title': "Email Verification Successful",
                'content': "Thank you for verifying your email with CiviWiki",
                'link': redirect_link
            }
            return TemplateResponse(request, 'general-message.html', template_var)
    else:
        # invalid link
        redirect_link = {
            'href': "/",
            'label': "Back to Main"
        }
        template_var = {
            'title': "Email Verification Error",
            'content': "Email could not be verified",
            'link': redirect_link
        }
        return TemplateResponse(request, 'general-message.html', template_var)


def recover_user():
    view_variables = {
        'template_name': 'user/reset_by_email.html',
        'post_reset_redirect': 'recovery_email_sent',
        'email_template_name': 'email/base_text_template.txt',
        'subject_template_name': 'email/base_email_template.html',
        'password_reset_form': RecoverUserForm
    }

    return view_variables


def password_reset_confirm():
    view_variables = {
        'template_name': 'user/password_reset.html',
        'set_password_form': PasswordResetForm
    }

    return view_variables


def recover_user_sent(request):
    redirect_link = {
        'href': "/",
        'label': "Back to Main"
    }

    template_var = {
        'title': "Email Sent",
        'content': ("We've emailed you your username and instructions for setting your password. "
                    "If an account exists with the email you entered, you should receive them shortly. "
                    "If you don't receive an email, please make sure you've entered the address you registered with, "
                    "and check your spam folder."),
        # TODO: move to string templates
        'link': redirect_link
    }
    return TemplateResponse(request, 'general-message.html', template_var)


def password_reset_complete(request):
    redirect_link = {
        'href': "/login",
        'label': "Login"
    }

    template_var = {
        'title': "Password reset complete",
        'content': "Your password has been set. You may now go ahead and login.",
        'link': redirect_link
    }
    return TemplateResponse(request, 'general-message.html', template_var)
