import json

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from api.models import Category, Account, Thread, Civi, Activity, Invitation
from api.forms import UpdateProfileImage
from core.constants import US_STATES
from core.custom_decorators import beta_blocker, login_required, full_account


def base_view(request):
    if not request.user.is_authenticated:
        return TemplateResponse(request, 'static_templates/landing.html', {})

    a = Account.objects.get(user=request.user)
    if not a.beta_access:
        return HttpResponseRedirect('/beta')
    if not a.full_account:
        return HttpResponseRedirect('/setup')
    if 'login_user_image' not in request.session.keys():
        request.session["login_user_image"] = a.profile_image_thumb_url

    categories = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]

    all_categories = list(Category.objects.values_list('id', flat=True))
    user_categories = list(a.categories.values_list('id', flat=True)) or all_categories

    feed_threads = [Thread.objects.summarize(t) for t in Thread.objects.exclude(is_draft=True).order_by('-created')]
    top5_threads = list(Thread.objects.filter(is_draft=False).order_by('-num_views')[:5].values('id', 'title'))
    my_draft_threads = [Thread.objects.summarize(t) for t in
                        Thread.objects.filter(author_id=a.id).exclude(is_draft=False).order_by('-created')]

    states = sorted(US_STATES, key=lambda s: s[1])
    data = {
        'categories': categories,
        'states': states,
        'user_categories': user_categories,
        'threads': feed_threads,
        'trending': top5_threads,
        'draft_threads': my_draft_threads
    }

    return TemplateResponse(request, 'feed.html', {'data': json.dumps(data)})


@login_required
@beta_blocker
@full_account
def user_profile(request, username=None):
    if not username:
        return HttpResponseRedirect('/profile/{0}'.format(request.user))
    else:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseRedirect('/404')
    data = {
        'username': user,
        'profile_image_form': UpdateProfileImage,
        'google_map_api_key': settings.GOOGLE_API_KEY,
        'sunlight_api_key': settings.SUNLIGHT_API_KEY
    }
    return TemplateResponse(request, 'account.html', data)


@login_required
@beta_blocker
def user_setup(request):
    a = Account.objects.get(user=request.user)
    if a.full_account:
        return HttpResponseRedirect('/')
        # start temp rep rendering TODO: REMOVE THIS
    else:
        data = {
            'username': request.user.username,
            'email': request.user.email,
            'google_map_api_key': settings.GOOGLE_API_KEY,
            'sunlight_api_key': settings.SUNLIGHT_API_KEY
        }
        return TemplateResponse(request, 'user-setup.html', data)


@login_required
@beta_blocker
@full_account
def issue_thread(request, thread_id=None):
    if not thread_id:
        return HttpResponseRedirect('/404')

    req_acct = Account.objects.get(user=request.user)
    t = Thread.objects.get(id=thread_id)
    c_qs = Civi.objects.filter(thread_id=thread_id).exclude(c_type='response')
    c_scored = [c.dict_with_score(req_acct.id) for c in c_qs]
    civis = sorted(c_scored, key=lambda c: c['score'], reverse=True)

    # modify thread view count
    t.num_civis = len(civis)
    t.num_views = F('num_views') + 1
    t.save()
    t.refresh_from_db()

    thread_wiki_data = {
        "thread_id": thread_id,
        "title": t.title,
        "summary": t.summary,
        "image": t.image_url,
        "author": {
            "username": t.author.user.username,
            "profile_image": t.author.profile_image_url,
            "first_name": t.author.first_name,
            "last_name": t.author.last_name
        },
        "contributors": [Account.objects.chip_summarize(a) for a in
                         Account.objects.filter(pk__in=c_qs.distinct('author').values_list('author', flat=True))],
        "category": {
            "id": t.category.id,
            "name": t.category.name
        },
        "categories": [{'id': c.id, 'name': c.name} for c in Category.objects.all()],
        "states": sorted(US_STATES, key=lambda s: s[1]),
        "created": t.created_date_str,
        "level": t.level,
        "state": t.state if t.level == "state" else "",
        "location": t.level if not t.state else dict(US_STATES).get(t.state),
        "num_civis": t.num_civis,
        "num_views": t.num_views,
        'user_votes': [{'civi_id': act.civi.id, 'activity_type': act.activity_type, 'c_type': act.civi.c_type} for act
                       in Activity.objects.filter(thread=t.id, account=req_acct.id)]
    }
    thread_body_data = {
        'civis': civis,
    }

    data = {
        'thread_id': thread_id,
        'is_draft': t.is_draft,
        'thread_wiki_data': json.dumps(thread_wiki_data),
        'thread_body_data': json.dumps(thread_body_data)
    }
    return TemplateResponse(request, 'thread.html', data)


@login_required
@beta_blocker
@full_account
def create_group(request):
    return TemplateResponse(request, 'newgroup.html', {})


@login_required
@user_passes_test(lambda u: u.is_staff)
def invite(request):
    user = User.objects.get(username=request.user.username)

    invitations = Invitation.objects.filter_by_host(host_user=user).order_by("-date_created").all()
    invitees = [invitation.summarize() for invitation in invitations]
    response_data = {
        'invitees': json.dumps(invitees)
    }

    return TemplateResponse(request, 'invite.html', response_data)


@login_required
@beta_blocker
def settings_view(request):
    request_account = Account.objects.get(user=request.user)

    response_data = {
        'username': request.user.username,
        'email': request.user.email,
        'google_map_api_key': settings.GOOGLE_API_KEY,
        'sunlight_api_key': settings.SUNLIGHT_API_KEY,
        'lng': request_account.longitude,
        'lat': request_account.latitude
    }

    return TemplateResponse(request, 'user/settings.html', response_data)


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            return HttpResponseRedirect('/')

    return TemplateResponse(request, 'login.html', {})


def beta_register(request, email='', token=''):
    if not email or not token:
        return HttpResponse('ERROR: BAD REQUEST')

    try:
        db_invite = Invitation.objects.get(invitee_email=email)
    except Invitation.DoesNotExist:
        return HttpResponse('ERROR: NO INVITATIONS EXIST FOR THIS EMAIL')

    if db_invite.verification_code != token:
        return HttpResponse('ERROR: BAD TOKEN')

    is_registered = User.objects.filter(email=email).exists()

    if is_registered:
        # registered and has been given beta access
        if request.user.is_authenticated:
            invitee_user = request.user
        else:
            invitee_user = User.objects.get(email=email)

        account = Account.objects.get(user=invitee_user)
        if account.beta_access:
            redirect_link = {
                'href': "/",
                'label': "Go to CiviWiki"
            }
            template_var = {
                'title': "Already Registered for Beta",
                'content': "You have already registered for a beta account",
                'link': redirect_link
            }
            return TemplateResponse(request, 'general-message.html', template_var)
        # registered but was not given beta access
        else:
            invitation = Invitation.objects.get(invitee_email=email)
            invitation.invitee_user = invitee_user
            invitation.save()

            account = Account.objects.get(user=invitee_user)
            account.beta_access = True
            account.save()

            redirect_link = {
                'href': "/",
                'label': "Go to CiviWiki"
            }
            template_var = {
                'title': "Beta Access Granted",
                'content': "You have now been granted beta access",
                'link': redirect_link
            }
            return TemplateResponse(request, 'general-message.html', template_var)

    template_var = {
        'email': email,
        'beta_token': token
    }

    return TemplateResponse(request, 'beta_register.html', template_var)


def beta_view(request):
    return TemplateResponse(request, 'beta_blocker.html', {})


def declaration(request):
    return TemplateResponse(request, 'declaration.html', {})


def landing_view(request):
    return TemplateResponse(request, 'static_templates/landing.html', {})


def how_it_works_view(request):
    return TemplateResponse(request, 'static_templates/how_it_works.html', {})


def about_view(request):
    return TemplateResponse(request, 'static_templates/about.html', {})


def support_us_view(request):
    return TemplateResponse(request, 'static_templates/support_us.html', {})


""" CSV export function. Thread ID goes in, CSV HTTP response attachment goes out. """


@csrf_exempt
def civi2csv(request, thread_id):
    import csv
    thread = thread_id
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + thread + '.csv'
    writer = csv.writer(response, delimiter=',')
    for card in Civi.objects.filter(thread_id=thread):
        data = []
        for key, value in card.dict_with_score().items():
            if value:
                data.append(value)
        writer.writerow(data)
    return response
