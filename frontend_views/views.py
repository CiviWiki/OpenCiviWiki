import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.db.models import F
from api.models import Category, Account, Thread, Civi, Activity
from api.forms import UpdateProfileImage

# from legislation import sunlightapi as sun
from utils.custom_decorators import beta_blocker, login_required, full_account
from utils.constants import US_STATES

def base_view(request):
    if not request.user.is_authenticated():
        return TemplateResponse(request, 'static_templates/landing.html', {})

    a = Account.objects.get(user=request.user)
    if not a.beta_access:
        return HttpResponseRedirect('/beta')
    if not a.full_account:
        return HttpResponseRedirect('/setup')

    categories = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]

    all_categories = list(Category.objects.values_list('id', flat=True))
    user_categories = list(a.categories.values_list('id', flat=True)) or all_categories

    feed_threads = [Thread.objects.summarize(t) for t in Thread.objects.order_by('-created')]
    top5_threads = list(Thread.objects.all().order_by('-num_views')[:5].values('id', 'title'))


    states = sorted(US_STATES, key=lambda s: s[1])
    data = {
        'categories': categories,
        'states': states,
        'user_categories': user_categories,
        'threads': feed_threads,
        'trending': top5_threads
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
        #start temp rep rendering TODO: REMOVE THIS
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
    # c_scored = Civi.objects.thread_sorted_by_score(c_qs, req_acct.id)
    c_scored = [c.dict_with_score(req_acct.id) for c in c_qs]
    civis = sorted(c_scored, key=lambda c: c['score'], reverse=True)


    # civis = Civi.objects.filter(thread_id=thread_id)
    # c = civis.order_by('-created')
    # c_scores = [ci.score(req_a.id) for ci in c]
    # c_data = [Civi.objects.serialize_s(ci) for ci in c]
    # for idx, item in enumerate(c_data):
    #     c_data[idx]['score'] = c_scores[idx]
    # c_data = sorted(c_data, key=lambda x: x['score'], reverse=True)

    #modify thread view count
    t.num_civis = len(civis)
    t.num_views = F('num_views') + 1
    t.save()
    t.refresh_from_db()

    thread_wiki_data = {
        "title": t.title,
        "summary": t.summary,
        "image": t.image_url,
        "author": {
            "username": t.author.user.username,
            "profile_image": t.author.profile_image_url,
            "first_name": t.author.first_name,
            "last_name": t.author.last_name
        },
        "contributors": [Account.objects.chip_summarize(a) for a in Account.objects.filter(pk__in=c_qs.distinct('author').values_list('author', flat=True))],
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
        'user_votes': [{'civi_id':act.civi.id, 'activity_type': act.activity_type, 'c_type': act.civi.c_type} for act in Activity.objects.filter(thread=t.id, account=req_acct.id)]
    }
    thread_body_data = {
        'civis': civis,
    }

    data = {
        'thread_id': thread_id,
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
@beta_blocker
@full_account
def dbview(request):
    result = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]

    return TemplateResponse(request, 'dbview.html', {'result': json.dumps(result)})


@login_required
@beta_blocker
@full_account
def add_civi(request):
    categories = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]
    topics = [{'id': c.id, 'topic': c.topic} for c in Topic.objects.all()]

    return TemplateResponse(request, 'add_civi.html', {'categories': json.dumps(categories), 'topics': json.dumps(topics)})


def login_view(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            return HttpResponseRedirect('/')

    return TemplateResponse(request, 'login.html', {})

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

def does_not_exist(request):
    return TemplateResponse(request, 'base/404.html', {})
